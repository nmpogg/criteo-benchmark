import argparse
import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow.parquet as pq


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = str(
    PROJECT_ROOT / "data/part-00015-99c339d5-fbac-4110-9dcf-75453a61a5c1.c000.snappy.parquet"
)
DEFAULT_OUTPUT = str(PROJECT_ROOT / "output/ctr_events.jsonl")
LABEL_COLUMN = "label"


def clean_value(value: Any) -> Any:
    if value is None:
        return None

    if pd.isna(value):
        return None

    if isinstance(value, float) and math.isnan(value):
        return None

    return value


def build_event(row: dict[str, Any], event_index: int) -> dict[str, Any]:
    features = {
        column: clean_value(value)
        for column, value in row.items()
        if column != LABEL_COLUMN
    }

    return {
        "event_id": f"evt_{event_index:09d}_{uuid.uuid4().hex[:8]}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "features": features,
    }


def convert_parquet_to_jsonl(
    input_path: Path,
    output_path: Path,
    batch_size: int,
    limit: int | None,
) -> int:
    parquet_file = pq.ParquetFile(input_path)
    columns = [
        column
        for column in parquet_file.schema.names
        if column != LABEL_COLUMN
    ]

    if not columns:
        raise ValueError(f"No feature columns found after dropping '{LABEL_COLUMN}'")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_events = 0
    with output_path.open("w", encoding="utf-8") as output_file:
        for record_batch in parquet_file.iter_batches(
            batch_size=batch_size,
            columns=columns,
        ):
            batch_df = record_batch.to_pandas()

            for row in batch_df.to_dict(orient="records"):
                if limit is not None and total_events >= limit:
                    return total_events

                event = build_event(row, total_events)
                output_file.write(
                    json.dumps(event, ensure_ascii=False, allow_nan=False)
                )
                output_file.write("\n")
                total_events += 1

    return total_events


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert CTR parquet data to JSON Lines events without label."
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help=f"Input parquet path. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output JSONL path. Default: {DEFAULT_OUTPUT}",
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
        help="Optional max number of events to write, useful for testing.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input parquet file not found: {input_path}")

    total_events = convert_parquet_to_jsonl(
        input_path=input_path,
        output_path=output_path,
        batch_size=args.batch_size,
        limit=args.limit,
    )

    print(f"Wrote {total_events} JSON events to {output_path}")


if __name__ == "__main__":
    main()
