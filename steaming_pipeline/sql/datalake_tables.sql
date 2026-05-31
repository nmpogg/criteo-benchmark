CREATE TABLE IF NOT EXISTS ctr_lake_daily_summary (
    summary_date DATE NOT NULL,
    model_version TEXT NOT NULL DEFAULT 'DCN_DHE_best',
    event_count BIGINT NOT NULL,
    avg_ctr_score DOUBLE PRECISION,
    predicted_click_count BIGINT NOT NULL,
    predicted_click_rate DOUBLE PRECISION,
    first_event_at TIMESTAMPTZ,
    last_event_at TIMESTAMPTZ,
    refreshed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (summary_date, model_version)
);

CREATE INDEX IF NOT EXISTS idx_ctr_lake_daily_summary_date
    ON ctr_lake_daily_summary (summary_date DESC);

CREATE TABLE IF NOT EXISTS ctr_lake_hourly_summary (
    bucket_start TIMESTAMPTZ NOT NULL,
    model_version TEXT NOT NULL DEFAULT 'DCN_DHE_best',
    event_count BIGINT NOT NULL,
    avg_ctr_score DOUBLE PRECISION,
    predicted_click_count BIGINT NOT NULL,
    predicted_click_rate DOUBLE PRECISION,
    refreshed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bucket_start, model_version)
);

CREATE INDEX IF NOT EXISTS idx_ctr_lake_hourly_summary_bucket
    ON ctr_lake_hourly_summary (bucket_start DESC);
