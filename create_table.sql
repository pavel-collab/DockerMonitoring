CREATE TABLE container_stats (
    container_id TEXT,
    cpu_usage DOUBLE PRECISION,
    memory_usage DOUBLE PRECISION,
    time TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

SELECT create_hypertable('container_stats', 'time');

CREATE VIEW dashboard_table AS
SELECT
    container_id,
    AVG(cpu_usage) AS avg_cpu_usage,
    AVG(memory_usage) AS avg_memory_usage,
    MAX("time") AS last_update_time
FROM container_stats
GROUP BY container_id;