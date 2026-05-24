from pathlib import Path
from typing import Any

import requests

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
DEFAULT_PROCESSED_FEATURES_PATH = str(PROJECT_ROOT / "data/lake/processed_features")


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


def predict_and_persist_micro_batch(
    batch_df,
    batch_id: int,
    model_url: str,
    model_batch_size: int,
    processed_features_path: str,
    postgres_dsn: str,
    model_version: str,
) -> None:
    if batch_df.rdd.isEmpty():
        print(f"batch_id={batch_id}: no events")
        return

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
    inserted = upsert_predictions(records, postgres_dsn)
    insert_batch_metrics(
        batch_id=batch_id,
        predictions=list(prediction_by_event_id.values()),
        model_version=model_version,
        postgres_dsn=postgres_dsn,
    )
    print(f"batch_id={batch_id}: upserted {inserted} predictions to PostgreSQL")
