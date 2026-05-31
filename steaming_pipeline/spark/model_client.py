from pathlib import Path
from typing import Any
from datetime import datetime, timezone

import requests
from pyspark.sql.functions import coalesce, col, to_date
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

from schemas import FEATURE_COLUMNS
from postgres_sink import (
    DEFAULT_MODEL_VERSION,
    DEFAULT_POSTGRES_DSN,
    insert_batch_metrics,
    row_to_prediction_record,
    upsert_predictions,
)


DEFAULT_MODEL_URL = "http://127.0.0.1:8000/predict-batch"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_EVENTS_PATH = str(PROJECT_ROOT / "data/lake/raw_events")
DEFAULT_PROCESSED_FEATURES_PATH = str(PROJECT_ROOT / "data/lake/processed_features")
DEFAULT_PREDICTION_EVENTS_PATH = str(PROJECT_ROOT / "data/lake/predictions")


def row_to_event(row) -> dict[str, Any]:
    row_dict = row.asDict(recursive=True)
    features = {
        feature_name: row_dict[feature_name]
        for feature_name in FEATURE_COLUMNS
    }

    return {
        "event_id": row_dict["event_id"],
        "features": features,
    }


def predict_batch(events: list[dict[str, Any]], model_url: str) -> list[dict[str, Any]]:
    if not events:
        return []

    response = requests.post(
        model_url,
        json={"events": events},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["predictions"]


def iter_chunks(items: list[dict[str, Any]], chunk_size: int):
    for start in range(0, len(items), chunk_size):
        yield items[start:start + chunk_size]


def predict_micro_batch(batch_df, batch_id: int, model_url: str, model_batch_size: int) -> None:
    events = [row_to_event(row) for row in batch_df.collect()]

    if not events:
        print(f"batch_id={batch_id}: no events")
        return

    print(f"batch_id={batch_id}: sending {len(events)} events to model")
    total_predictions = 0

    for chunk in iter_chunks(events, model_batch_size):
        predictions = predict_batch(chunk, model_url)
        total_predictions += len(predictions)
        for prediction in predictions[:5]:
            print(
                "prediction "
                f"event_id={prediction['event_id']} "
                f"ctr_score={prediction['ctr_score']:.6f} "
                f"prediction_label={prediction['prediction_label']}"
            )

    print(f"batch_id={batch_id}: received {total_predictions} predictions")


def write_processed_features(batch_df, output_path: str) -> int:
    if batch_df.rdd.isEmpty():
        return 0

    (
        batch_df.write.mode("append")
        .partitionBy("event_date")
        .parquet(output_path)
    )
    return batch_df.count()


def write_raw_events(batch_df, output_path: str) -> int:
    if batch_df.rdd.isEmpty():
        return 0

    raw_df = (
        batch_df.select(
            "event_id",
            "event_timestamp",
            "event_time",
            coalesce(col("event_date"), to_date("processing_time")).alias("event_date"),
            "processing_time",
            col("topic").alias("kafka_topic"),
            col("partition").alias("kafka_partition"),
            col("offset").alias("kafka_offset"),
            "kafka_timestamp",
            "raw_json",
        )
    )

    (
        raw_df.write.mode("append")
        .partitionBy("event_date")
        .parquet(output_path)
    )
    return raw_df.count()


def build_prediction_event_schema() -> StructType:
    return StructType(
        [
            StructField("event_id", StringType(), False),
            StructField("event_timestamp", TimestampType(), True),
            StructField("processing_time", TimestampType(), True),
            StructField("kafka_topic", StringType(), True),
            StructField("kafka_partition", IntegerType(), True),
            StructField("kafka_offset", LongType(), True),
            StructField("ctr_score", DoubleType(), False),
            StructField("prediction_label", IntegerType(), False),
            StructField("model_version", StringType(), False),
            StructField("raw_event", StringType(), True),
            StructField("features", StringType(), True),
        ]
    )


def to_spark_timestamp(value: Any) -> Any:
    if not isinstance(value, datetime):
        return value
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def write_prediction_events(batch_df, records: list[dict[str, Any]], output_path: str) -> int:
    if not records:
        return 0

    spark_records = []
    for record in records:
        spark_record = dict(record)
        spark_record["event_timestamp"] = to_spark_timestamp(record.get("event_timestamp"))
        spark_record["processing_time"] = to_spark_timestamp(record.get("processing_time"))
        spark_records.append(spark_record)

    prediction_df = batch_df.sparkSession.createDataFrame(
        spark_records,
        schema=build_prediction_event_schema(),
    ).withColumn(
        "event_date",
        to_date(coalesce(col("event_timestamp"), col("processing_time"))),
    )

    (
        prediction_df.write.mode("append")
        .partitionBy("event_date")
        .parquet(output_path)
    )
    return prediction_df.count()


def predict_and_persist_micro_batch(
    batch_df,
    batch_id: int,
    model_url: str,
    model_batch_size: int,
    raw_events_path: str,
    processed_features_path: str,
    prediction_events_path: str,
    postgres_dsn: str,
    model_version: str,
) -> None:
    if batch_df.rdd.isEmpty():
        print(f"batch_id={batch_id}: no events")
        return

    raw_count = write_raw_events(batch_df, raw_events_path)
    print(f"batch_id={batch_id}: wrote {raw_count} raw event rows to {raw_events_path}")

    feature_count = write_processed_features(batch_df, processed_features_path)
    print(
        f"batch_id={batch_id}: wrote {feature_count} processed feature rows "
        f"to {processed_features_path}"
    )

    rows = batch_df.collect()
    events = [row_to_event(row) for row in rows]
    prediction_by_event_id: dict[str, dict[str, Any]] = {}

    print(f"batch_id={batch_id}: sending {len(events)} events to model")
    for chunk in iter_chunks(events, model_batch_size):
        for prediction in predict_batch(chunk, model_url):
            prediction_by_event_id[prediction["event_id"]] = prediction
            if len(prediction_by_event_id) <= 5:
                print(
                    "prediction "
                    f"event_id={prediction['event_id']} "
                    f"ctr_score={prediction['ctr_score']:.6f} "
                    f"prediction_label={prediction['prediction_label']}"
                )

    records = [
        row_to_prediction_record(row, prediction_by_event_id[row.event_id], model_version)
        for row in rows
        if row.event_id in prediction_by_event_id
    ]
    lake_prediction_count = write_prediction_events(batch_df, records, prediction_events_path)
    print(
        f"batch_id={batch_id}: wrote {lake_prediction_count} prediction rows "
        f"to {prediction_events_path}"
    )

    inserted = upsert_predictions(records, postgres_dsn)
    insert_batch_metrics(
        batch_id=batch_id,
        predictions=list(prediction_by_event_id.values()),
        model_version=model_version,
        postgres_dsn=postgres_dsn,
    )
    print(f"batch_id={batch_id}: upserted {inserted} predictions to PostgreSQL")
