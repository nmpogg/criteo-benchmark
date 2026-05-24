import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
from fastapi import FastAPI
from pydantic import BaseModel

from model_service.dcn_dhe import DCN_DHE


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models/DCN_DHE_best.pt"
CATEGORY_MAPPING_PATH = PROJECT_ROOT / "model_service/artifacts/category_mapping.json"

NUMERICAL_FEATURES = [f"integer_feature_{index}" for index in range(1, 14)]
CATEGORICAL_FEATURES = [f"categorical_feature_{index}" for index in range(1, 27)]

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
THRESHOLD = 0.5


class PredictEvent(BaseModel):
    event_id: str
    features: dict[str, Any]


class PredictBatchRequest(BaseModel):
    events: list[PredictEvent]


app = FastAPI(title="CTR DCN-DHE Model Service")
model: DCN_DHE | None = None
category_mapping: dict[str, dict[str, int]] = {}


def load_category_mapping() -> dict[str, dict[str, int]]:
    if not CATEGORY_MAPPING_PATH.exists():
        raise FileNotFoundError(
            f"Missing category mapping: {CATEGORY_MAPPING_PATH}. "
            "Run scripts/build_category_mapping.py first."
        )

    with CATEGORY_MAPPING_PATH.open("r", encoding="utf-8") as mapping_file:
        return json.load(mapping_file)


def build_model(mapping: dict[str, dict[str, int]]) -> DCN_DHE:
    vocab_sizes = [
        max(len(mapping[feature_name]), 1)
        for feature_name in CATEGORICAL_FEATURES
    ]
    dcn = DCN_DHE(
        num_dense=len(NUMERICAL_FEATURES),
        vocab_sizes=vocab_sizes,
        embed_dim=64,
        cross_layers=3,
        hidden_dims=(512, 512),
        dhe_num_hashes=1024,
        dhe_hidden=(512, 256),
    )
    state_dict = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=True)
    dcn.load_state_dict(state_dict)
    dcn.to(DEVICE)
    dcn.eval()
    return dcn


@app.on_event("startup")
def startup() -> None:
    global model, category_mapping
    category_mapping = load_category_mapping()
    model = build_model(category_mapping)


def numerical_value(features: dict[str, Any], feature_name: str) -> float:
    value = features.get(feature_name, 0.0)
    if value is None:
        return 0.0
    return float(value)


def categorical_id(features: dict[str, Any], feature_name: str) -> int:
    value = features.get(feature_name, "UNKNOWN")
    if value is None:
        value = "UNKNOWN"
    return category_mapping[feature_name].get(str(value), 0)


def prepare_tensors(events: list[PredictEvent]) -> tuple[torch.Tensor, torch.Tensor]:
    dense_rows = [
        [
            numerical_value(event.features, feature_name)
            for feature_name in NUMERICAL_FEATURES
        ]
        for event in events
    ]
    sparse_rows = [
        [
            categorical_id(event.features, feature_name)
            for feature_name in CATEGORICAL_FEATURES
        ]
        for event in events
    ]

    dense_tensor = torch.tensor(np.asarray(dense_rows), dtype=torch.float32, device=DEVICE)
    sparse_tensor = torch.tensor(np.asarray(sparse_rows), dtype=torch.long, device=DEVICE)
    return dense_tensor, sparse_tensor


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "device": str(DEVICE),
    }


@app.post("/predict-batch")
@torch.no_grad()
def predict_batch(request: PredictBatchRequest) -> dict[str, Any]:
    if model is None:
        raise RuntimeError("Model is not loaded")

    if not request.events:
        return {"predictions": []}

    dense_tensor, sparse_tensor = prepare_tensors(request.events)
    logits = model(dense_tensor, sparse_tensor).squeeze(1)
    scores = torch.sigmoid(logits).detach().cpu().numpy().tolist()

    predictions = [
        {
            "event_id": event.event_id,
            "ctr_score": float(score),
            "prediction_label": int(score >= THRESHOLD),
        }
        for event, score in zip(request.events, scores)
    ]
    return {"predictions": predictions}
