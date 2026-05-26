CREATE TABLE IF NOT EXISTS ctr_predictions (
    event_id TEXT PRIMARY KEY,
    event_timestamp TIMESTAMPTZ,
    processing_time TIMESTAMPTZ,
    kafka_topic TEXT,
    kafka_partition INTEGER,
    kafka_offset BIGINT,
    ctr_score DOUBLE PRECISION NOT NULL,
    prediction_label INTEGER NOT NULL,
    model_version TEXT NOT NULL DEFAULT 'DCN_DHE_best',
    raw_event JSONB,
    features JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_ctr_predictions_created_at
    ON ctr_predictions (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_ctr_predictions_event_timestamp
    ON ctr_predictions (event_timestamp DESC);

CREATE TABLE IF NOT EXISTS ctr_prediction_metrics (
    id BIGSERIAL PRIMARY KEY,
    batch_id BIGINT NOT NULL,
    event_count INTEGER NOT NULL,
    avg_ctr_score DOUBLE PRECISION,
    click_prediction_count INTEGER NOT NULL,
    model_version TEXT NOT NULL DEFAULT 'DCN_DHE_best',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_ctr_prediction_metrics_created_at
    ON ctr_prediction_metrics (created_at DESC);
