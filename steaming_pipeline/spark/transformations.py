import json
from pathlib import Path

from pyspark.sql.functions import col, current_timestamp, from_json, to_date, to_timestamp

from schemas import CATEGORICAL_FEATURES, FEATURE_COLUMNS, NUMERICAL_FEATURES, build_event_schema


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FEATURE_DEFAULTS_PATH = PROJECT_ROOT / "spark/feature_defaults.json"


def load_feature_defaults(path: str | Path = DEFAULT_FEATURE_DEFAULTS_PATH) -> dict:
    with Path(path).open("r", encoding="utf-8") as defaults_file:
        return json.load(defaults_file)


def parse_kafka_events(kafka_df):
    event_schema = build_event_schema()

    parsed_df = (
        kafka_df.selectExpr(
            "CAST(key AS STRING) AS kafka_key",
            "CAST(value AS STRING) AS raw_json",
            "topic",
            "partition",
            "offset",
            "timestamp AS kafka_timestamp",
        )
        .withColumn("event", from_json(col("raw_json"), event_schema))
        .where(col("event").isNotNull())
        .where(col("event.event_id").isNotNull())
    )

    return parsed_df.select(
        col("event.event_id").alias("event_id"),
        col("event.timestamp").alias("event_timestamp"),
        col("event.features").alias("features"),
        "topic",
        "partition",
        "offset",
        "kafka_timestamp",
        "raw_json",
    )


def flatten_events(parsed_df):
    feature_columns = [
        col(f"features.{feature_name}").alias(feature_name)
        for feature_name in FEATURE_COLUMNS
    ]

    return parsed_df.select(
        "event_id",
        "event_timestamp",
        to_timestamp("event_timestamp").alias("event_time"),
        to_date(to_timestamp("event_timestamp")).alias("event_date"),
        current_timestamp().alias("processing_time"),
        "topic",
        "partition",
        "offset",
        "kafka_timestamp",
        "raw_json",
        *feature_columns,
    )


def clean_features(flattened_df, feature_defaults: dict):
    numerical_medians = feature_defaults["numerical_medians"]
    categorical_default = feature_defaults["categorical_default"]

    fill_values = {
        feature_name: float(numerical_medians[feature_name])
        for feature_name in NUMERICAL_FEATURES
    }
    fill_values.update(
        {
            feature_name: categorical_default
            for feature_name in CATEGORICAL_FEATURES
        }
    )

    return flattened_df.fillna(fill_values)


def select_console_columns(processed_df):
    return processed_df.select(
        "event_id",
        "event_timestamp",
        "event_time",
        "event_date",
        "processing_time",
        "topic",
        "partition",
        "offset",
        *FEATURE_COLUMNS,
    )
