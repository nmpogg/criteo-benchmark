import argparse
import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "data/part-00015-99c339d5-fbac-4110-9dcf-75453a61a5c1.c000.snappy.parquet"
DEFAULT_OUTPUT = PROJECT_ROOT / "model_service/artifacts/category_mapping.json"
CATEGORICAL_FEATURES = [f"categorical_feature_{index}" for index in range(1, 27)]


def build_mapping(input_path: Path) -> dict:
    df = pd.read_parquet(input_path, columns=CATEGORICAL_FEATURES)
    mapping = {}

    for feature_name in CATEGORICAL_FEATURES:
        series = df[feature_name].where(df[feature_name].notna(), "UNKNOWN").astype(str)
        values = sorted(series.unique().tolist())
        mapping[feature_name] = {
            value: index
            for index, value in enumerate(values)
        }

    return mapping


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build categorical string-to-id mapping for CTR model inference."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help=f"Input parquet path. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help=f"Output mapping JSON path. Default: {DEFAULT_OUTPUT}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input parquet file not found: {input_path}")

    mapping = build_mapping(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(mapping, ensure_ascii=False),
        encoding="utf-8",
    )

    vocab_sizes = {
        feature_name: len(feature_mapping)
        for feature_name, feature_mapping in mapping.items()
    }
    print(f"Wrote category mapping to {output_path}")
    print(f"Vocab sizes: {vocab_sizes}")


if __name__ == "__main__":
    main()
