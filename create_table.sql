CREATE TABLE container_stats (
    container_id TEXT,
    cpu_usage DOUBLE PRECISION,
    memory_usage DOUBLE PRECISION,
    time TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

SELECT create_hypertable('container_stats', 'time');
