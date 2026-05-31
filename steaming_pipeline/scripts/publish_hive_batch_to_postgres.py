import argparse
import csv
import subprocess
from io import StringIO
from typing import Any


DEFAULT_POSTGRES_DSN = "dbname=ctr_db user=ctr_user password=ctr_pass host=127.0.0.1 port=5433"
BEELINE_COMMAND = [
    "docker",
    "compose",
    "exec",
    "-T",
    "hive-server",
    "beeline",
    "-u",
    "jdbc:hive2://localhost:10000/default",
    "--silent=true",
    "--showHeader=false",
    "--outputformat=csv2",
]


DAILY_SQL = """
SELECT
  CAST(event_date AS STRING) AS summary_date,
  model_version,
  COUNT(1) AS event_count,
  AVG(ctr_score) AS avg_ctr_score,
  SUM(CAST(prediction_label AS BIGINT)) AS predicted_click_count,
  SUM(CAST(prediction_label AS DOUBLE)) / COUNT(1) AS predicted_click_rate,
  CAST(MIN(event_timestamp) AS STRING) AS first_event_at,
  CAST(MAX(event_timestamp) AS STRING) AS last_event_at
FROM ctr_lake.predictions
GROUP BY event_date, model_version
ORDER BY summary_date, model_version
"""


HOURLY_SQL = """
SELECT
  from_unixtime(CAST(FLOOR(unix_timestamp(COALESCE(event_timestamp, processing_time)) / 3600) * 3600 AS BIGINT)) AS bucket_start,
  model_version,
  COUNT(1) AS event_count,
  AVG(ctr_score) AS avg_ctr_score,
  SUM(CAST(prediction_label AS BIGINT)) AS predicted_click_count,
  SUM(CAST(prediction_label AS DOUBLE)) / COUNT(1) AS predicted_click_rate
FROM ctr_lake.predictions
WHERE COALESCE(event_timestamp, processing_time) IS NOT NULL
GROUP BY
  from_unixtime(CAST(FLOOR(unix_timestamp(COALESCE(event_timestamp, processing_time)) / 3600) * 3600 AS BIGINT)),
  model_version
ORDER BY bucket_start, model_version
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Hive batch summaries and publish the result to PostgreSQL for Grafana."
    )
    parser.add_argument(
        "--postgres-dsn",
        default=DEFAULT_POSTGRES_DSN,
        help=f"PostgreSQL DSN. Default: {DEFAULT_POSTGRES_DSN}",
    )
    return parser.parse_args()


def run_hive_query(sql: str, expected_columns: int) -> list[list[str]]:
    completed = subprocess.run(
        [*BEELINE_COMMAND, "-e", sql],
        check=True,
        capture_output=True,
        text=True,
    )
    prompt_marker = "jdbc:hive2://localhost:10000/default>"
    cleaned_lines = []
    for line in completed.stdout.splitlines():
        if prompt_marker in line:
            line = line.split(prompt_marker, 1)[1].strip()
        cleaned_lines.append(line)

    raw_output = "\n".join(
        line
        for line in cleaned_lines
        if line.strip()
        and not line.startswith("Connecting to")
        and not line.startswith("Connected to")
        and not line.startswith("Driver:")
        and not line.startswith("Transaction isolation:")
        and not line.startswith("Beeline version")
        and not line.startswith("Closing:")
        and not line.startswith("0:")
    )
    if not raw_output.strip():
        return []

    return [
        row
        for row in csv.reader(StringIO(raw_output))
        if row and len(row) == expected_columns and not row[0].startswith("No rows")
    ]


def optional_float(value: str) -> float | None:
    if value == "" or value.lower() == "null":
        return None
    return float(value)


def optional_text(value: str) -> str | None:
    if value == "" or value.lower() == "null":
        return None
    return value


def int_value(value: str) -> int:
    if value == "" or value.lower() == "null":
        return 0
    return int(float(value))


def publish_daily(rows: list[list[str]], postgres_dsn: str) -> None:
    if not rows:
        print("No daily rows returned from Hive")
        return

    import psycopg2
    from psycopg2.extras import execute_values

    values: list[tuple[Any, ...]] = [
        (
            optional_text(row[0]),
            optional_text(row[1]),
            int_value(row[2]),
            optional_float(row[3]),
            int_value(row[4]),
            optional_float(row[5]),
            optional_text(row[6]),
            optional_text(row[7]),
        )
        for row in rows
    ]

    sql = """
        INSERT INTO ctr_lake_daily_summary (
            summary_date,
            model_version,
            event_count,
            avg_ctr_score,
            predicted_click_count,
            predicted_click_rate,
            first_event_at,
            last_event_at
        )
        VALUES %s
        ON CONFLICT (summary_date, model_version) DO UPDATE SET
            event_count = EXCLUDED.event_count,
            avg_ctr_score = EXCLUDED.avg_ctr_score,
            predicted_click_count = EXCLUDED.predicted_click_count,
            predicted_click_rate = EXCLUDED.predicted_click_rate,
            first_event_at = EXCLUDED.first_event_at,
            last_event_at = EXCLUDED.last_event_at,
            refreshed_at = CURRENT_TIMESTAMP
    """

    with psycopg2.connect(postgres_dsn) as conn:
        with conn.cursor() as cursor:
            execute_values(cursor, sql, values)

    print(f"Published {len(values)} daily rows to PostgreSQL")


def publish_hourly(rows: list[list[str]], postgres_dsn: str) -> None:
    if not rows:
        print("No hourly rows returned from Hive")
        return

    import psycopg2
    from psycopg2.extras import execute_values

    values: list[tuple[Any, ...]] = [
        (
            optional_text(row[0]),
            optional_text(row[1]),
            int_value(row[2]),
            optional_float(row[3]),
            int_value(row[4]),
            optional_float(row[5]),
        )
        for row in rows
    ]

    sql = """
        INSERT INTO ctr_lake_hourly_summary (
            bucket_start,
            model_version,
            event_count,
            avg_ctr_score,
            predicted_click_count,
            predicted_click_rate
        )
        VALUES %s
        ON CONFLICT (bucket_start, model_version) DO UPDATE SET
            event_count = EXCLUDED.event_count,
            avg_ctr_score = EXCLUDED.avg_ctr_score,
            predicted_click_count = EXCLUDED.predicted_click_count,
            predicted_click_rate = EXCLUDED.predicted_click_rate,
            refreshed_at = CURRENT_TIMESTAMP
    """

    with psycopg2.connect(postgres_dsn) as conn:
        with conn.cursor() as cursor:
            execute_values(cursor, sql, values)

    print(f"Published {len(values)} hourly rows to PostgreSQL")


def main() -> None:
    args = parse_args()

    print("Run Hive daily summary query")
    daily_rows = run_hive_query(DAILY_SQL, expected_columns=8)
    publish_daily(daily_rows, args.postgres_dsn)

    print("Run Hive hourly summary query")
    hourly_rows = run_hive_query(HOURLY_SQL, expected_columns=6)
    publish_hourly(hourly_rows, args.postgres_dsn)


if __name__ == "__main__":
    main()
