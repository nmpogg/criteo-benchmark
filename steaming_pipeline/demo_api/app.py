import json
import os
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import pyarrow.parquet as pq
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRODUCER_DIR = PROJECT_ROOT / "producer"
SPARK_DIR = PROJECT_ROOT / "spark"
DEMO_WEB_DIR = PROJECT_ROOT / "demo_web"
UPLOAD_DIR = PROJECT_ROOT / "data/uploads"
FEATURE_DEFAULTS_PATH = SPARK_DIR / "feature_defaults.json"
DEFAULT_KAFKA_BOOTSTRAP = "127.0.0.1:9092"
DEFAULT_TOPIC = "ctr_events"
DEFAULT_MODEL_URL = "http://127.0.0.1:8000/predict-batch"
DEFAULT_POSTGRES_DSN = os.environ.get(
    "CTR_POSTGRES_DSN",
    "dbname=ctr_db user=ctr_user password=ctr_pass host=127.0.0.1 port=5433",
)
DEFAULT_MODEL_VERSION = os.environ.get("CTR_MODEL_VERSION", "DCN_DHE_best")
RAW_EVENTS_PATH = PROJECT_ROOT / "data/lake/raw_events"
PROCESSED_FEATURES_PATH = PROJECT_ROOT / "data/lake/processed_features"
PREDICTION_EVENTS_PATH = PROJECT_ROOT / "data/lake/predictions"
DATALAKE_SYNC_SCRIPT = PROJECT_ROOT / "scripts/sync_lake_to_hdfs_hive.sh"
HIVE_PUBLISH_SCRIPT = PROJECT_ROOT / "scripts/publish_hive_batch_to_postgres.py"
HDFS_LAKE_ROOT = "/user/ctr/lake"
HDFS_UI_URL = "http://127.0.0.1:9870"
HIVE_JDBC_URL = "jdbc:hive2://localhost:10000/ctr_lake"
HIVE_DBEAVER_HINT = "DBeaver Hive: localhost:10000, database ctr_lake, auth none"
GRAFANA_BATCH_URL = "http://127.0.0.1:3000/d/ctr-batch-lake/ctr-batch-data-lake-reports"
DOWNSTREAM_MONITOR_TIMEOUT_SECONDS = int(os.environ.get("CTR_DEMO_MONITOR_TIMEOUT_SECONDS", "120"))
DOWNSTREAM_MONITOR_INTERVAL_SECONDS = float(os.environ.get("CTR_DEMO_MONITOR_INTERVAL_SECONDS", "2"))
AUTO_SYNC_DATALAKE = os.environ.get("CTR_DEMO_AUTO_SYNC_DATALAKE", "1") != "0"
DATALAKE_COMMAND_TIMEOUT_SECONDS = int(os.environ.get("CTR_DEMO_DATALAKE_COMMAND_TIMEOUT_SECONDS", "300"))

sys.path.insert(0, str(PRODUCER_DIR))
sys.path.insert(0, str(SPARK_DIR))

from parquet_to_json_events import LABEL_COLUMN, build_event  # noqa: E402
from schemas import FEATURE_COLUMNS  # noqa: E402


STAGE_DEFINITIONS = [
    ("upload", "Web Dashboard", "Upload parquet"),
    ("api", "Web API", "FastAPI backend"),
    ("storage", "Uploaded Parquet", "data/uploads"),
    ("producer", "Kafka Producer", "Parquet -> JSON"),
    ("kafka", "Kafka Topic", "ctr_events"),
    ("spark", "Spark Streaming", "Consume Kafka + clean features"),
    ("model", "Model Service", "Called by Spark"),
    ("data_lake", "Local Data Lake", "Bronze/Silver/Gold parquet"),
    ("hdfs", "HDFS", "/user/ctr/lake"),
    ("hive", "Hive", "External tables + partitions"),
    ("postgres", "PostgreSQL", "Predictions"),
    ("batch_report", "Batch Reports", "Hive summary -> PostgreSQL"),
    ("dashboard", "Web/Grafana", "Read PostgreSQL"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_stage_state() -> dict[str, dict[str, Any]]:
    return {
        stage_id: {
            "id": stage_id,
            "name": name,
            "description": description,
            "status": "pending",
            "detail": "",
            "updated_at": None,
        }
        for stage_id, name, description in STAGE_DEFINITIONS
    }


runs: dict[str, dict[str, Any]] = {}
runs_lock = threading.Lock()


def create_run(
    filename: str,
    limit: int,
    send_to_kafka: bool,
    model_url: str,
    sleep_seconds: float,
) -> dict[str, Any]:
    run_id = uuid.uuid4().hex[:12]
    run = {
        "run_id": run_id,
        "filename": filename,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "status": "queued",
        "limit": limit,
        "send_to_kafka": send_to_kafka,
        "model_url": model_url,
        "sleep_seconds": sleep_seconds,
        "stages": new_stage_state(),
        "metrics": {
            "rows": 0,
            "columns": 0,
            "features": 0,
            "requested_events": limit,
            "events_built": 0,
            "events_sent": 0,
            "send_rate_eps": None,
            "processed_events": 0,
            "lake_rows": 0,
            "raw_lake_files": 0,
            "processed_lake_files": 0,
            "prediction_lake_files": 0,
            "hdfs_zones": 0,
            "model_batches": 0,
            "predictions": 0,
            "postgres_rows": 0,
            "kafka_offsets": 0,
            "avg_ctr": None,
            "click_rate": None,
            "duration_seconds": 0,
        },
        "schema": [],
        "raw_events": [],
        "processed_events": [],
        "predictions": [],
        "feature_changes": [],
        "logs": [],
        "errors": [],
    }
    with runs_lock:
        runs[run_id] = run
    return run


def get_run(run_id: str) -> dict[str, Any]:
    with runs_lock:
        run = runs.get(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
        return json.loads(json.dumps(run))


def mutate_run(run_id: str, mutator) -> None:
    with runs_lock:
        run = runs[run_id]
        mutator(run)
        run["updated_at"] = now_iso()


def log(run_id: str, message: str) -> None:
    def apply(run: dict[str, Any]) -> None:
        run["logs"].append({"time": now_iso(), "message": message})
        run["logs"] = run["logs"][-160:]

    mutate_run(run_id, apply)


def set_stage(run_id: str, stage_id: str, status: str, detail: str = "") -> None:
    def apply(run: dict[str, Any]) -> None:
        stage = run["stages"][stage_id]
        stage["status"] = status
        stage["detail"] = detail
        stage["updated_at"] = now_iso()

    mutate_run(run_id, apply)


def fail_run(run_id: str, stage_id: str, exc: Exception) -> None:
    message = str(exc)

    def apply(run: dict[str, Any]) -> None:
        run["status"] = "error"
        run["errors"].append(message)
        run["stages"][stage_id]["status"] = "error"
        run["stages"][stage_id]["detail"] = message
        run["stages"][stage_id]["updated_at"] = now_iso()

    mutate_run(run_id, apply)
    log(run_id, f"ERROR {stage_id}: {message}")


def parquet_metadata(path: Path) -> tuple[pq.ParquetFile, list[str]]:
    parquet_file = pq.ParquetFile(path)
    columns = parquet_file.schema.names
    return parquet_file, columns


def sample_events(path: Path, limit: int, run_id: str | None = None) -> list[dict[str, Any]]:
    parquet_file = pq.ParquetFile(path)
    columns = [column for column in parquet_file.schema.names if column != LABEL_COLUMN]
    if not columns:
        raise ValueError(f"No feature columns found after dropping '{LABEL_COLUMN}'")

    events: list[dict[str, Any]] = []
    for record_batch in parquet_file.iter_batches(batch_size=max(limit, 1), columns=columns):
        batch_df = record_batch.to_pandas()
        for row in batch_df.to_dict(orient="records"):
            event = build_event(row, len(events))
            if run_id is not None:
                event["event_id"] = f"{run_id}_{event['event_id']}"
            events.append(event)
            if len(events) >= limit:
                return events
    return events


def count_parquet_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*.parquet") if item.is_file())


def update_lake_file_metrics(run_id: str) -> dict[str, int]:
    counts = {
        "raw_lake_files": count_parquet_files(RAW_EVENTS_PATH),
        "processed_lake_files": count_parquet_files(PROCESSED_FEATURES_PATH),
        "prediction_lake_files": count_parquet_files(PREDICTION_EVENTS_PATH),
    }
    mutate_run(run_id, lambda run: run["metrics"].update(counts))
    return counts


def command_summary(completed: subprocess.CompletedProcess[str], max_lines: int = 18) -> str:
    output = "\n".join(
        line
        for text in (completed.stdout, completed.stderr)
        for line in text.splitlines()
        if line.strip()
    )
    lines = output.splitlines()
    return "\n".join(lines[-max_lines:]) if lines else "(no output)"


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=DATALAKE_COMMAND_TIMEOUT_SECONDS,
        check=True,
    )


def sync_datalake_to_hdfs_hive(run_id: str) -> None:
    if not AUTO_SYNC_DATALAKE:
        set_stage(run_id, "hdfs", "skipped", "CTR_DEMO_AUTO_SYNC_DATALAKE=0")
        set_stage(run_id, "hive", "skipped", "Auto sync disabled")
        set_stage(run_id, "batch_report", "skipped", "Auto batch publish disabled")
        return

    lake_counts = update_lake_file_metrics(run_id)
    set_stage(
        run_id,
        "data_lake",
        "done",
        (
            f"local parquet raw={lake_counts['raw_lake_files']}, "
            f"silver={lake_counts['processed_lake_files']}, "
            f"gold={lake_counts['prediction_lake_files']}"
        ),
    )

    if not DATALAKE_SYNC_SCRIPT.exists():
        raise FileNotFoundError(f"Missing Data Lake sync script: {DATALAKE_SYNC_SCRIPT}")

    set_stage(run_id, "hdfs", "running", f"Syncing local lake to {HDFS_LAKE_ROOT}")
    set_stage(run_id, "hive", "pending", "Waiting for HDFS sync")
    log(run_id, "Syncing local Data Lake parquet files to HDFS and repairing Hive partitions")
    completed = run_command(["bash", str(DATALAKE_SYNC_SCRIPT)])
    log(run_id, "HDFS/Hive sync finished:\n" + command_summary(completed))
    mutate_run(run_id, lambda run: run["metrics"].update({"hdfs_zones": 3}))
    set_stage(run_id, "hdfs", "done", f"Browse in NameNode UI: {HDFS_UI_URL}")
    set_stage(run_id, "hive", "done", f"Query with {HIVE_DBEAVER_HINT}")

    if not HIVE_PUBLISH_SCRIPT.exists():
        set_stage(run_id, "batch_report", "skipped", "Hive publish script missing")
        return

    set_stage(run_id, "batch_report", "running", "Publishing Hive daily/hourly summary to PostgreSQL")
    log(run_id, "Running Hive batch aggregation and publishing summary tables for Grafana")
    try:
        completed = run_command(
            [
                sys.executable,
                str(HIVE_PUBLISH_SCRIPT),
                "--postgres-dsn",
                DEFAULT_POSTGRES_DSN,
            ]
        )
    except subprocess.CalledProcessError as exc:
        log(run_id, "Hive batch publish failed:\n" + command_summary(exc))
        set_stage(run_id, "batch_report", "error", "Hive summary publish did not finish")
        return

    log(run_id, "Hive batch publish finished:\n" + command_summary(completed))
    set_stage(run_id, "batch_report", "done", f"Grafana batch dashboard: {GRAFANA_BATCH_URL}")


def send_prebuilt_events_to_kafka(
    events: list[dict[str, Any]],
    bootstrap_servers: str = DEFAULT_KAFKA_BOOTSTRAP,
    topic: str = DEFAULT_TOPIC,
    sleep_seconds: float = 0.0,
    progress_callback: Callable[[int], None] | None = None,
) -> int:
    if not events:
        return 0

    from kafka import KafkaProducer

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        key_serializer=lambda key: key.encode("utf-8"),
        value_serializer=lambda event: json.dumps(
            event,
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8"),
        acks="all",
        retries=5,
        linger_ms=10,
    )

    total_sent = 0
    try:
        for event in events:
            producer.send(topic, key=event["event_id"], value=event)
            total_sent += 1
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
            if total_sent % 1000 == 0:
                producer.flush()
                if progress_callback is not None:
                    progress_callback(total_sent)
        producer.flush()
        if progress_callback is not None:
            progress_callback(total_sent)
    finally:
        producer.close()

    return total_sent


def fetch_downstream_status(run_id: str, postgres_dsn: str = DEFAULT_POSTGRES_DSN) -> dict[str, Any]:
    import psycopg2

    event_pattern = f"{run_id}_%"
    with psycopg2.connect(postgres_dsn) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*)::integer AS prediction_count,
                    COALESCE(AVG(ctr_score), 0) AS avg_ctr,
                    COALESCE(AVG(prediction_label::double precision), 0) AS click_rate,
                    COUNT(kafka_offset)::integer AS kafka_offsets
                FROM ctr_predictions
                WHERE event_id LIKE %s
                """,
                (event_pattern,),
            )
            prediction_count, avg_ctr, click_rate, kafka_offsets = cursor.fetchone()

            cursor.execute(
                """
                SELECT
                    event_id,
                    ctr_score,
                    prediction_label,
                    model_version,
                    kafka_topic,
                    kafka_partition,
                    kafka_offset,
                    created_at
                FROM ctr_predictions
                WHERE event_id LIKE %s
                ORDER BY created_at DESC
                LIMIT 20
                """,
                (event_pattern,),
            )
            latest = [
                {
                    "event_id": row[0],
                    "ctr_score": float(row[1]),
                    "prediction_label": int(row[2]),
                    "model_version": row[3],
                    "kafka_topic": row[4],
                    "kafka_partition": row[5],
                    "kafka_offset": row[6],
                    "created_at": row[7].isoformat() if row[7] is not None else None,
                }
                for row in cursor.fetchall()
            ]

    return {
        "prediction_count": int(prediction_count),
        "avg_ctr": float(avg_ctr),
        "click_rate": float(click_rate),
        "kafka_offsets": int(kafka_offsets),
        "latest": latest,
    }


def update_downstream_monitoring(
    run_id: str,
    expected_events: int,
    start_time: float,
    final: bool = False,
) -> int:
    status = fetch_downstream_status(run_id)
    prediction_count = status["prediction_count"]
    is_complete = prediction_count >= expected_events

    def apply(run: dict[str, Any]) -> None:
        run["predictions"] = status["latest"]
        run["processed_events"] = status["latest"][:1]
        run["metrics"].update(
            {
                "processed_events": prediction_count,
                "lake_rows": prediction_count,
                "predictions": prediction_count,
                "postgres_rows": prediction_count,
                "kafka_offsets": status["kafka_offsets"],
                "avg_ctr": status["avg_ctr"] if prediction_count else None,
                "click_rate": status["click_rate"] if prediction_count else None,
                "duration_seconds": round(time.monotonic() - start_time, 2),
            }
        )

    mutate_run(run_id, apply)

    if prediction_count == 0:
        set_stage(run_id, "spark", "running", "Waiting for Spark to consume Kafka")
        set_stage(run_id, "model", "pending", "Spark will call model service")
        set_stage(run_id, "data_lake", "pending", "Spark will write bronze/silver/gold parquet")
        set_stage(run_id, "hdfs", "pending", "Waiting for local Data Lake output")
        set_stage(run_id, "hive", "pending", "Waiting for HDFS sync")
        set_stage(run_id, "postgres", "pending", "Waiting for predictions")
        set_stage(run_id, "batch_report", "pending", "Waiting for Hive tables")
    else:
        lake_counts = update_lake_file_metrics(run_id)
        detail = f"{prediction_count:,}/{expected_events:,} predictions visible in PostgreSQL"
        stage_status = "done" if is_complete else "running"
        set_stage(run_id, "spark", stage_status, detail)
        set_stage(run_id, "model", stage_status, detail)
        set_stage(
            run_id,
            "data_lake",
            stage_status,
            (
                f"local parquet raw={lake_counts['raw_lake_files']}, "
                f"silver={lake_counts['processed_lake_files']}, "
                f"gold={lake_counts['prediction_lake_files']}"
            ),
        )
        set_stage(run_id, "postgres", stage_status, detail)

    if is_complete:
        set_stage(run_id, "dashboard", "done", "Web and Grafana can read PostgreSQL")
    elif final:
        set_stage(run_id, "dashboard", "running", f"Monitoring timed out at {prediction_count:,}/{expected_events:,}")
    else:
        set_stage(run_id, "dashboard", "running", "Polling PostgreSQL")

    return prediction_count


def run_pipeline(run_id: str, uploaded_path: Path) -> None:
    start_time = time.monotonic()

    try:
        mutate_run(run_id, lambda run: run.update({"status": "running"}))
        set_stage(run_id, "upload", "done", "File received from dashboard")
        set_stage(run_id, "api", "running", "Inspecting parquet")
        log(run_id, f"Run started. run_id={run_id}")
        log(run_id, f"Uploaded file saved: {uploaded_path}")

        log(run_id, "Reading parquet metadata")
        parquet_file, columns = parquet_metadata(uploaded_path)
        row_count = parquet_file.metadata.num_rows
        feature_columns = [column for column in columns if column != LABEL_COLUMN]
        missing_expected = [name for name in FEATURE_COLUMNS if name not in feature_columns]

        def store_inspection(run: dict[str, Any]) -> None:
            run["schema"] = columns
            run["metrics"].update(
                {
                    "rows": row_count,
                    "columns": len(columns),
                    "features": len(feature_columns),
                }
            )

        mutate_run(run_id, store_inspection)
        set_stage(run_id, "api", "done", f"{row_count:,} rows, {len(columns)} columns")
        set_stage(run_id, "storage", "done", str(uploaded_path.relative_to(PROJECT_ROOT)))
        if missing_expected:
            log(run_id, f"Warning: missing expected features: {', '.join(missing_expected[:8])}")
        log(run_id, f"Parquet schema inspected: {row_count:,} rows, {len(columns)} columns")

        run_snapshot = get_run(run_id)
        event_limit = max(1, min(int(run_snapshot["limit"]), row_count))
        mutate_run(run_id, lambda run: run["metrics"].update({"requested_events": event_limit}))
        set_stage(run_id, "producer", "running", f"Building {event_limit:,} JSON events")
        log(run_id, f"Building {event_limit:,} events from the top of uploaded parquet")
        raw_events = sample_events(uploaded_path, event_limit, run_id=run_id)

        mutate_run(
            run_id,
            lambda run: (
                run.update({"raw_events": raw_events[:10]}),
                run["metrics"].update({"events_built": len(raw_events)}),
            ),
        )
        set_stage(run_id, "producer", "done", f"{len(raw_events):,} events built")
        log(run_id, f"Producer converted selected rows into {len(raw_events)} JSON events")
        if raw_events:
            log(run_id, f"Event id range: first={raw_events[0]['event_id']} last={raw_events[-1]['event_id']}")

        kafka_handoff_done = False
        if run_snapshot["send_to_kafka"]:
            set_stage(run_id, "kafka", "running", f"Sending {len(raw_events):,} events")
            try:
                sleep_seconds = max(0.0, float(run_snapshot.get("sleep_seconds", 0.0)))
                expected_send_seconds = sleep_seconds * len(raw_events)
                log(
                    run_id,
                    f"Connecting to Kafka bootstrap={DEFAULT_KAFKA_BOOTSTRAP}, topic={DEFAULT_TOPIC}, "
                    f"sleep_seconds={sleep_seconds}",
                )
                if sleep_seconds > 0:
                    log(run_id, f"Realtime pacing enabled. Expected send time about {expected_send_seconds:.2f}s")

                last_logged_sent = {"value": 0}
                send_start = time.monotonic()

                def report_kafka_progress(total_sent: int) -> None:
                    if total_sent == last_logged_sent["value"]:
                        return
                    last_logged_sent["value"] = total_sent
                    elapsed = max(time.monotonic() - send_start, 0.001)
                    send_rate = total_sent / elapsed
                    mutate_run(run_id, lambda run: run["metrics"].update({"events_sent": total_sent}))
                    mutate_run(run_id, lambda run: run["metrics"].update({"send_rate_eps": send_rate}))
                    set_stage(
                        run_id,
                        "kafka",
                        "running",
                        f"Sent {total_sent:,}/{len(raw_events):,} events ({send_rate:.1f} events/s)",
                    )
                    log(run_id, f"Kafka send progress: {total_sent:,}/{len(raw_events):,} events ({send_rate:.1f} events/s)")

                total_sent = send_prebuilt_events_to_kafka(
                    raw_events,
                    sleep_seconds=sleep_seconds,
                    progress_callback=report_kafka_progress,
                )
                kafka_handoff_done = total_sent == len(raw_events)
                mutate_run(run_id, lambda run: run["metrics"].update({"events_sent": total_sent}))
                set_stage(run_id, "kafka", "done", f"{total_sent:,} events sent to {DEFAULT_TOPIC}")
                log(run_id, f"Kafka producer sent {total_sent} events to topic {DEFAULT_TOPIC}")
            except Exception as exc:
                set_stage(run_id, "kafka", "error", str(exc))
                log(run_id, f"Kafka send failed: {exc}")
        else:
            set_stage(run_id, "kafka", "skipped", "Kafka send disabled for this run")
            set_stage(run_id, "spark", "skipped", "No Kafka events for Spark")
            set_stage(run_id, "model", "skipped", "Spark did not receive this run")
            set_stage(run_id, "data_lake", "skipped", "Spark did not receive this run")
            set_stage(run_id, "hdfs", "skipped", "No new Data Lake output")
            set_stage(run_id, "hive", "skipped", "No new Data Lake output")
            set_stage(run_id, "postgres", "skipped", "No downstream predictions")
            set_stage(run_id, "batch_report", "skipped", "No downstream predictions")
            set_stage(run_id, "dashboard", "done", "Ingestion-only run finished")
            log(run_id, "Kafka send skipped")

        if kafka_handoff_done:
            log(run_id, "FastAPI handoff complete. Waiting for Spark/PostgreSQL output.")
            deadline = time.monotonic() + DOWNSTREAM_MONITOR_TIMEOUT_SECONDS
            prediction_count = 0
            last_logged_prediction_count = -1
            while time.monotonic() < deadline:
                try:
                    prediction_count = update_downstream_monitoring(
                        run_id,
                        expected_events=len(raw_events),
                        start_time=start_time,
                    )
                except Exception as exc:
                    set_stage(run_id, "postgres", "error", str(exc))
                    log(run_id, f"PostgreSQL monitor failed: {exc}")
                    break

                if prediction_count != last_logged_prediction_count:
                    last_logged_prediction_count = prediction_count
                    log(
                        run_id,
                        f"Downstream progress: {prediction_count:,}/{len(raw_events):,} predictions visible in PostgreSQL",
                    )

                if prediction_count >= len(raw_events):
                    log(run_id, f"Spark/PostgreSQL completed {prediction_count} predictions")
                    break
                time.sleep(DOWNSTREAM_MONITOR_INTERVAL_SECONDS)

            if prediction_count < len(raw_events):
                try:
                    update_downstream_monitoring(
                        run_id,
                        expected_events=len(raw_events),
                        start_time=start_time,
                        final=True,
                    )
                except Exception as exc:
                    set_stage(run_id, "postgres", "error", str(exc))
                    log(run_id, f"Final PostgreSQL monitor failed: {exc}")
                log(
                    run_id,
                    f"Downstream monitor stopped at {prediction_count}/{len(raw_events)} predictions. "
                    "Check that Spark realtime job and model service are running.",
                )

            if prediction_count > 0:
                try:
                    sync_datalake_to_hdfs_hive(run_id)
                except Exception as exc:
                    set_stage(run_id, "hdfs", "error", str(exc))
                    set_stage(run_id, "hive", "error", "Data Lake sync did not finish")
                    set_stage(run_id, "batch_report", "error", "Hive summary publish did not finish")
                    log(run_id, f"Data Lake HDFS/Hive sync failed: {exc}")

        def finish(run: dict[str, Any]) -> None:
            has_errors = any(stage["status"] == "error" for stage in run["stages"].values())
            has_running = any(stage["status"] == "running" for stage in run["stages"].values())
            has_pending = any(stage["status"] == "pending" for stage in run["stages"].values())
            run["status"] = "completed_with_warnings" if has_errors or has_running or has_pending else "completed"
            run["metrics"]["duration_seconds"] = round(time.monotonic() - start_time, 2)

        mutate_run(run_id, finish)
        log(run_id, "Ingestion run finished")
    except Exception as exc:
        fail_run(run_id, "api", exc)


app = FastAPI(title="CTR Streaming Demo API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "upload_dir": str(UPLOAD_DIR),
        "kafka_topic": DEFAULT_TOPIC,
        "model_url": DEFAULT_MODEL_URL,
        "postgres_dsn": DEFAULT_POSTGRES_DSN,
        "raw_events_path": str(RAW_EVENTS_PATH),
        "processed_features_path": str(PROCESSED_FEATURES_PATH),
        "prediction_events_path": str(PREDICTION_EVENTS_PATH),
        "hdfs_lake_root": HDFS_LAKE_ROOT,
        "hdfs_ui_url": HDFS_UI_URL,
        "hive_jdbc_url": HIVE_JDBC_URL,
        "hive_dbeaver_hint": HIVE_DBEAVER_HINT,
        "grafana_batch_url": GRAFANA_BATCH_URL,
        "auto_sync_datalake": AUTO_SYNC_DATALAKE,
    }


@app.post("/api/demo/upload")
async def upload_demo_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    limit: int = Form(100),
    send_to_kafka: bool = Form(True),
    sleep_seconds: float = Form(0.02),
    inference_url: str = Form(DEFAULT_MODEL_URL, alias="model_url"),
) -> dict[str, Any]:
    if not file.filename or not file.filename.endswith(".parquet"):
        raise HTTPException(status_code=400, detail="Please upload a .parquet file")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename).name
    safe_sleep_seconds = max(0.0, min(float(sleep_seconds), 5.0))
    run = create_run(
        safe_name,
        max(1, min(limit, 10_000)),
        send_to_kafka,
        inference_url,
        safe_sleep_seconds,
    )
    target = UPLOAD_DIR / f"{run['run_id']}_{safe_name}"

    bytes_written = 0
    with target.open("wb") as output_file:
        while chunk := await file.read(1024 * 1024):
            output_file.write(chunk)
            bytes_written += len(chunk)

    log(
        run["run_id"],
        f"Upload received: filename={safe_name}, bytes={bytes_written:,}, limit={run['limit']}, "
        f"send_to_kafka={send_to_kafka}, sleep_seconds={safe_sleep_seconds}",
    )

    background_tasks.add_task(run_pipeline, run["run_id"], target)
    return {"run_id": run["run_id"], "status_url": f"/api/demo/runs/{run['run_id']}"}


@app.get("/api/demo/runs")
def list_runs() -> dict[str, Any]:
    with runs_lock:
        items = [
            {
                "run_id": run["run_id"],
                "filename": run["filename"],
                "status": run["status"],
                "created_at": run["created_at"],
                "updated_at": run["updated_at"],
            }
            for run in runs.values()
        ]
    return {"runs": sorted(items, key=lambda item: item["created_at"], reverse=True)}


@app.get("/api/demo/runs/{run_id}")
def run_status(run_id: str) -> dict[str, Any]:
    return get_run(run_id)


app.mount("/", StaticFiles(directory=str(DEMO_WEB_DIR), html=True), name="demo_web")
