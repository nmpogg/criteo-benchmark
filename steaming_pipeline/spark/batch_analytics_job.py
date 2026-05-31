import argparse
from pathlib import Path
from typing import Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    avg,
    coalesce,
    col,
    count,
    date_trunc,
    max as spark_max,
    min as spark_min,
    sum as spark_sum,
    to_date,
)

from model_client import DEFAULT_PREDICTION_EVENTS_PATH
from postgres_sink import DEFAULT_POSTGRES_DSN


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MARTS_PATH = str(PROJECT_ROOT / "data/lake/marts")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build batch Data Lake marts from Spark prediction parquet files."
    )
    parser.add_argument(
        "--prediction-events-path",
        default=DEFAULT_PREDICTION_EVENTS_PATH,
        help=f"Gold prediction event parquet path. Default: {DEFAULT_PREDICTION_EVENTS_PATH}",
    )
    parser.add_argument(
        "--marts-path",
        default=DEFAULT_MARTS_PATH,
        help=f"Output path for batch mart parquet files. Default: {DEFAULT_MARTS_PATH}",
    )
    parser.add_argument(
        "--postgres-dsn",
        default=DEFAULT_POSTGRES_DSN,
        help="PostgreSQL DSN used when publishing batch summaries.",
    )
    parser.add_argument(
        "--skip-postgres",
        action="store_true",
        help="Only write parquet marts, do not publish batch summaries to PostgreSQL.",
    )
    return parser.parse_args()


def load_prediction_events(spark: SparkSession, prediction_events_path: str) -> DataFrame:
    if not Path(prediction_events_path).exists():
        raise FileNotFoundError(
            "Prediction Data Lake path does not exist yet: "
            f"{prediction_events_path}. Run the streaming job with --sink lake-model-postgres first."
        )

    df = spark.read.parquet(prediction_events_path)
    if "event_date" not in df.columns:
        df = df.withColumn("event_date", to_date(coalesce(col("event_timestamp"), col("processing_time"))))

    return df.where(col("event_id").isNotNull())


def build_daily_summary(predictions_df: DataFrame) -> DataFrame:
    grouped_df = predictions_df.groupBy("event_date", "model_version").agg(
        count("*").alias("event_count"),
        avg("ctr_score").alias("avg_ctr_score"),
        spark_sum(col("prediction_label").cast("long")).alias("predicted_click_count"),
        spark_min("event_timestamp").alias("first_event_at"),
        spark_max("event_timestamp").alias("last_event_at"),
    )

    return grouped_df.select(
        col("event_date").alias("summary_date"),
        "model_version",
        "event_count",
        "avg_ctr_score",
        "predicted_click_count",
        (col("predicted_click_count") / col("event_count")).alias("predicted_click_rate"),
        "first_event_at",
        "last_event_at",
    )


def build_hourly_summary(predictions_df: DataFrame) -> DataFrame:
    base_df = predictions_df.withColumn(
        "bucket_start",
        date_trunc("hour", coalesce(col("event_timestamp"), col("processing_time"))),
    ).where(col("bucket_start").isNotNull())

    grouped_df = base_df.groupBy("bucket_start", "model_version").agg(
        count("*").alias("event_count"),
        avg("ctr_score").alias("avg_ctr_score"),
        spark_sum(col("prediction_label").cast("long")).alias("predicted_click_count"),
    )

    return grouped_df.select(
        "bucket_start",
        "model_version",
        "event_count",
        "avg_ctr_score",
        "predicted_click_count",
        (col("predicted_click_count") / col("event_count")).alias("predicted_click_rate"),
    )


def write_parquet_marts(daily_df: DataFrame, hourly_df: DataFrame, marts_path: str) -> None:
    daily_path = str(Path(marts_path) / "daily_ctr_summary")
    hourly_path = str(Path(marts_path) / "hourly_ctr_summary")

    daily_df.write.mode("overwrite").parquet(daily_path)
    hourly_df.write.mode("overwrite").parquet(hourly_path)

    print(f"Wrote daily batch mart to {daily_path}")
    print(f"Wrote hourly batch mart to {hourly_path}")


def row_value(row: Any, key: str) -> Any:
    value = row[key]
    return value


def publish_daily_summary(daily_rows: list[Any], postgres_dsn: str) -> None:
    if not daily_rows:
        return

    import psycopg2
    from psycopg2.extras import execute_values

    values = [
        (
            row_value(row, "summary_date"),
            row_value(row, "model_version"),
            row_value(row, "event_count"),
            row_value(row, "avg_ctr_score"),
            row_value(row, "predicted_click_count"),
            row_value(row, "predicted_click_rate"),
            row_value(row, "first_event_at"),
            row_value(row, "last_event_at"),
        )
        for row in daily_rows
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


def publish_hourly_summary(hourly_rows: list[Any], postgres_dsn: str) -> None:
    if not hourly_rows:
        return

    import psycopg2
    from psycopg2.extras import execute_values

    values = [
        (
            row_value(row, "bucket_start"),
            row_value(row, "model_version"),
            row_value(row, "event_count"),
            row_value(row, "avg_ctr_score"),
            row_value(row, "predicted_click_count"),
            row_value(row, "predicted_click_rate"),
        )
        for row in hourly_rows
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


def publish_postgres_marts(daily_df: DataFrame, hourly_df: DataFrame, postgres_dsn: str) -> None:
    daily_rows = daily_df.collect()
    hourly_rows = hourly_df.collect()

    publish_daily_summary(daily_rows, postgres_dsn)
    publish_hourly_summary(hourly_rows, postgres_dsn)

    print(f"Published {len(daily_rows)} daily summary rows to PostgreSQL")
    print(f"Published {len(hourly_rows)} hourly summary rows to PostgreSQL")


def main() -> None:
    args = parse_args()
    spark = (
        SparkSession.builder.appName("CTRDataLakeBatchAnalytics")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    predictions_df = load_prediction_events(spark, args.prediction_events_path)
    daily_df = build_daily_summary(predictions_df).orderBy("summary_date", "model_version")
    hourly_df = build_hourly_summary(predictions_df).orderBy("bucket_start", "model_version")

    daily_count = daily_df.count()
    hourly_count = hourly_df.count()
    print(f"Built {daily_count} daily summary rows")
    print(f"Built {hourly_count} hourly summary rows")

    write_parquet_marts(daily_df, hourly_df, args.marts_path)

    if not args.skip_postgres:
        publish_postgres_marts(daily_df, hourly_df, args.postgres_dsn)

    spark.stop()


if __name__ == "__main__":
    main()
