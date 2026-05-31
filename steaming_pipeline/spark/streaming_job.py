import argparse
from pathlib import Path
from functools import partial

from pyspark.sql import SparkSession

from model_client import (
    DEFAULT_MODEL_URL,
    DEFAULT_MODEL_VERSION,
    DEFAULT_PREDICTION_EVENTS_PATH,
    DEFAULT_POSTGRES_DSN,
    DEFAULT_PROCESSED_FEATURES_PATH,
    DEFAULT_RAW_EVENTS_PATH,
    predict_and_persist_micro_batch,
    predict_micro_batch,
)
from transformations import (
    DEFAULT_FEATURE_DEFAULTS_PATH,
    clean_features,
    flatten_events,
    load_feature_defaults,
    parse_kafka_events,
    select_console_columns,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOTSTRAP_SERVERS = "127.0.0.1:9092"
DEFAULT_TOPIC = "ctr_events"
DEFAULT_CHECKPOINT_LOCATION = str(PROJECT_ROOT / "spark/checkpoint/ctr_events_console")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read CTR events from Kafka, preprocess features, and print to console."
    )
    parser.add_argument(
        "--bootstrap-servers",
        default=DEFAULT_BOOTSTRAP_SERVERS,
        help=f"Kafka bootstrap servers. Default: {DEFAULT_BOOTSTRAP_SERVERS}",
    )
    parser.add_argument(
        "--topic",
        default=DEFAULT_TOPIC,
        help=f"Kafka topic. Default: {DEFAULT_TOPIC}",
    )
    parser.add_argument(
        "--starting-offsets",
        default="latest",
        choices=["earliest", "latest"],
        help="Kafka starting offsets. Use earliest to read existing test events.",
    )
    parser.add_argument(
        "--checkpoint-location",
        default=DEFAULT_CHECKPOINT_LOCATION,
        help=f"Spark checkpoint location. Default: {DEFAULT_CHECKPOINT_LOCATION}",
    )
    parser.add_argument(
        "--feature-defaults",
        default=str(DEFAULT_FEATURE_DEFAULTS_PATH),
        help=f"Feature defaults JSON path. Default: {DEFAULT_FEATURE_DEFAULTS_PATH}",
    )
    parser.add_argument(
        "--trigger-processing-time",
        default="5 seconds",
        help="Structured Streaming processing trigger interval.",
    )
    parser.add_argument(
        "--available-now",
        action="store_true",
        help="Process currently available Kafka data once, then stop.",
    )
    parser.add_argument(
        "--sink",
        default="console",
        choices=["console", "model", "lake-model-postgres"],
        help=(
            "Output sink. Use console to inspect features, model to call CTR service, "
            "or lake-model-postgres to store processed features and predictions."
        ),
    )
    parser.add_argument(
        "--model-url",
        default=DEFAULT_MODEL_URL,
        help=f"Model service predict-batch URL. Default: {DEFAULT_MODEL_URL}",
    )
    parser.add_argument(
        "--model-batch-size",
        type=int,
        default=128,
        help="Number of events per request to model service.",
    )
    parser.add_argument(
        "--processed-features-path",
        default=DEFAULT_PROCESSED_FEATURES_PATH,
        help=(
            "Data Lake path for processed features when using lake-model-postgres. "
            f"Default: {DEFAULT_PROCESSED_FEATURES_PATH}"
        ),
    )
    parser.add_argument(
        "--raw-events-path",
        default=DEFAULT_RAW_EVENTS_PATH,
        help=(
            "Bronze Data Lake path for raw Kafka events when using lake-model-postgres. "
            f"Default: {DEFAULT_RAW_EVENTS_PATH}"
        ),
    )
    parser.add_argument(
        "--prediction-events-path",
        default=DEFAULT_PREDICTION_EVENTS_PATH,
        help=(
            "Gold Data Lake path for prediction events when using lake-model-postgres. "
            f"Default: {DEFAULT_PREDICTION_EVENTS_PATH}"
        ),
    )
    parser.add_argument(
        "--postgres-dsn",
        default=DEFAULT_POSTGRES_DSN,
        help="PostgreSQL DSN used when writing predictions.",
    )
    parser.add_argument(
        "--model-version",
        default=DEFAULT_MODEL_VERSION,
        help=f"Model version stored with predictions. Default: {DEFAULT_MODEL_VERSION}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    feature_defaults = load_feature_defaults(args.feature_defaults)

    spark = (
        SparkSession.builder.appName("CTRKafkaFeatureProcessor")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    kafka_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", args.bootstrap_servers)
        .option("subscribe", args.topic)
        .option("startingOffsets", args.starting_offsets)
        .load()
    )

    parsed_df = parse_kafka_events(kafka_df)
    flattened_df = flatten_events(parsed_df)
    processed_df = clean_features(flattened_df, feature_defaults)

    if args.sink == "console":
        writer = (
            select_console_columns(processed_df)
            .writeStream.format("console")
            .outputMode("append")
            .option("truncate", "false")
            .option("numRows", 20)
            .option("checkpointLocation", args.checkpoint_location)
        )
    elif args.sink == "model":
        writer = (
            processed_df.writeStream.foreachBatch(
                partial(
                    predict_micro_batch,
                    model_url=args.model_url,
                    model_batch_size=args.model_batch_size,
                )
            )
            .outputMode("append")
            .option("checkpointLocation", args.checkpoint_location)
        )
    else:
        writer = (
            processed_df.writeStream.foreachBatch(
                partial(
                    predict_and_persist_micro_batch,
                    model_url=args.model_url,
                    model_batch_size=args.model_batch_size,
                    raw_events_path=args.raw_events_path,
                    processed_features_path=args.processed_features_path,
                    prediction_events_path=args.prediction_events_path,
                    postgres_dsn=args.postgres_dsn,
                    model_version=args.model_version,
                )
            )
            .outputMode("append")
            .option("checkpointLocation", args.checkpoint_location)
        )

    if args.available_now:
        writer = writer.trigger(availableNow=True)
    else:
        writer = writer.trigger(processingTime=args.trigger_processing_time)

    query = writer.start()
    query.awaitTermination()


if __name__ == "__main__":
    main()
