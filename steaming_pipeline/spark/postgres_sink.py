import json
import os
from datetime import datetime
from typing import Any

try:
    from schemas import FEATURE_COLUMNS
except ModuleNotFoundError:
    from spark.schemas import FEATURE_COLUMNS


DEFAULT_POSTGRES_DSN = os.environ.get(
    "CTR_POSTGRES_DSN",
    "dbname=ctr_db user=ctr_user password=ctr_pass host=127.0.0.1 port=5433",
)
DEFAULT_MODEL_VERSION = os.environ.get("CTR_MODEL_VERSION", "DCN_DHE_best")


def _to_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)


def _to_datetime(value: Any) -> Any:
    if isinstance(value, datetime) or value is None:
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return value


def row_to_prediction_record(row, prediction: dict[str, Any], model_version: str) -> dict[str, Any]:
    row_dict = row.asDict(recursive=True)
    features = {
        feature_name: row_dict.get(feature_name)
        for feature_name in FEATURE_COLUMNS
    }
    raw_event = {
        "event_id": row_dict.get("event_id"),
        "timestamp": row_dict.get("event_timestamp"),
        "features": features,
    }

    return {
        "event_id": row_dict["event_id"],
        "event_timestamp": _to_datetime(row_dict.get("event_time") or row_dict.get("event_timestamp")),
        "processing_time": _to_datetime(row_dict.get("processing_time")),
        "kafka_topic": row_dict.get("topic"),
        "kafka_partition": row_dict.get("partition"),
        "kafka_offset": row_dict.get("offset"),
        "ctr_score": float(prediction["ctr_score"]),
        "prediction_label": int(prediction["prediction_label"]),
        "model_version": model_version,
        "raw_event": _to_json(raw_event),
        "features": _to_json(features),
    }


def upsert_predictions(records: list[dict[str, Any]], postgres_dsn: str = DEFAULT_POSTGRES_DSN) -> int:
    if not records:
        return 0

    import psycopg2
    from psycopg2.extras import execute_values

    sql = """
        INSERT INTO ctr_predictions (
            event_id,
            event_timestamp,
            processing_time,
            kafka_topic,
            kafka_partition,
            kafka_offset,
            ctr_score,
            prediction_label,
            model_version,
            raw_event,
            features
        )
        VALUES %s
        ON CONFLICT (event_id) DO UPDATE SET
            event_timestamp = EXCLUDED.event_timestamp,
            processing_time = EXCLUDED.processing_time,
            kafka_topic = EXCLUDED.kafka_topic,
            kafka_partition = EXCLUDED.kafka_partition,
            kafka_offset = EXCLUDED.kafka_offset,
            ctr_score = EXCLUDED.ctr_score,
            prediction_label = EXCLUDED.prediction_label,
            model_version = EXCLUDED.model_version,
            raw_event = EXCLUDED.raw_event,
            features = EXCLUDED.features,
            updated_at = CURRENT_TIMESTAMP
    """
    values = [
        (
            record["event_id"],
            record["event_timestamp"],
            record["processing_time"],
            record["kafka_topic"],
            record["kafka_partition"],
            record["kafka_offset"],
            record["ctr_score"],
            record["prediction_label"],
            record["model_version"],
            record["raw_event"],
            record["features"],
        )
        for record in records
    ]

    with psycopg2.connect(postgres_dsn) as conn:
        with conn.cursor() as cursor:
            execute_values(cursor, sql, values)

    return len(records)


def insert_batch_metrics(
    batch_id: int,
    predictions: list[dict[str, Any]],
    model_version: str,
    postgres_dsn: str = DEFAULT_POSTGRES_DSN,
) -> None:
    if not predictions:
        return

    import psycopg2

    avg_ctr = sum(float(item["ctr_score"]) for item in predictions) / len(predictions)
    click_count = sum(int(item["prediction_label"]) for item in predictions)

    with psycopg2.connect(postgres_dsn) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ctr_prediction_metrics (
                    batch_id,
                    event_count,
                    avg_ctr_score,
                    click_prediction_count,
                    model_version
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    batch_id,
                    len(predictions),
                    avg_ctr,
                    click_count,
                    model_version,
                ),
            )
