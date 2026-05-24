import argparse
import json
import time
from pathlib import Path
from typing import Any, Iterator

import pyarrow.parquet as pq

from parquet_to_json_events import DEFAULT_INPUT, LABEL_COLUMN, build_event


DEFAULT_BOOTSTRAP_SERVERS = "127.0.0.1:9092"
DEFAULT_TOPIC = "ctr_events"


def iter_events(
    input_path: Path,
    batch_size: int,
    limit: int | None,
) -> Iterator[dict[str, Any]]:
    parquet_file = pq.ParquetFile(input_path)
    columns = [
        column
        for column in parquet_file.schema.names
        if column != LABEL_COLUMN
    ]

    if not columns:
        raise ValueError(f"No feature columns found after dropping '{LABEL_COLUMN}'")

    total_events = 0
    for record_batch in parquet_file.iter_batches(
        batch_size=batch_size,
        columns=columns,
    ):
        batch_df = record_batch.to_pandas()

        for row in batch_df.to_dict(orient="records"):
            if limit is not None and total_events >= limit:
                return

            yield build_event(row, total_events)
            total_events += 1


def create_kafka_producer(bootstrap_servers: str):
    from kafka import KafkaProducer

    return KafkaProducer(
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


def send_events_to_kafka(
    input_path: Path,
    bootstrap_servers: str,
    topic: str,
    batch_size: int,
    limit: int | None,
    sleep_seconds: float,
) -> int:
    producer = create_kafka_producer(bootstrap_servers)
    total_sent = 0

    try:
        for event in iter_events(
            input_path=input_path,
            batch_size=batch_size,
            limit=limit,
        ):
            producer.send(topic, key=event["event_id"], value=event)
            total_sent += 1

            if total_sent % 1000 == 0:
                producer.flush()
                print(f"Sent {total_sent} events to topic '{topic}'")

            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

        producer.flush()
    finally:
        producer.close()

    return total_sent


def print_events(
    input_path: Path,
    batch_size: int,
    limit: int | None,
) -> int:
    total_events = 0
    for event in iter_events(
        input_path=input_path,
        batch_size=batch_size,
        limit=limit,
    ):
        print(json.dumps(event, ensure_ascii=False, allow_nan=False))
        total_events += 1

    return total_events


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send CTR parquet rows as JSON events to Kafka."
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help=f"Input parquet path. Default: {DEFAULT_INPUT}",
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
        "--batch-size",
        type=int,
        default=10_000,
        help="Number of parquet rows to process per batch.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional max number of events to send, useful for testing.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.0,
        help="Optional delay after each event to simulate realtime traffic.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print events instead of sending them to Kafka.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        raise FileNotFoundError(f"Input parquet file not found: {input_path}")

    if args.dry_run:
        total_events = print_events(
            input_path=input_path,
            batch_size=args.batch_size,
            limit=args.limit,
        )
        print(f"Printed {total_events} events")
        return

    total_sent = send_events_to_kafka(
        input_path=input_path,
        bootstrap_servers=args.bootstrap_servers,
        topic=args.topic,
        batch_size=args.batch_size,
        limit=args.limit,
        sleep_seconds=args.sleep_seconds,
    )
    print(f"Sent {total_sent} events to topic '{args.topic}'")


if __name__ == "__main__":
    main()
