-- создадим представление с аггрегацией статистики для заглавной веб-страницы
CREATE VIEW dashboard_table AS
SELECT
    id,
    AVG(cpu_usage) AS avg_cpu_usage,
    AVG(memory_usage) AS avg_memory_usage,
    MAX("time") AS last_update_time
FROM container_statistics
GROUP BY id;

-- создадим материализованное представление для наиболее интересных статистик
CREATE MATERIALIZED VIEW container_aggregation 
    WITH (timescaledb.continuous) AS 
        SELECT 
            id AS container_id,
            time_bucket('1 hour', time) AS bucket, 
            first(cpu_usage, time) AS fst_cpu_usg, 
            last(cpu_usage, time) AS lst_cpu_usg, 
            avg(cpu_usage) AS avg_cpu_usg, 
            first(memory_usage, time) AS fst_mem_usg, 
            last(memory_usage, time) AS lst_mem_usg, 
            avg(memory_usage) AS avg_mem_usg 
        FROM container_statistics 
        GROUP BY 
            container_id, 
            bucket;

-- настроим политику обновления статистик
SELECT add_continuous_aggregate_policy('container_aggregation', 
                                        start_offset => INTERVAL '3 hours', 
                                        end_offset => INTERVAL '1 hour', 
                                        schedule_interval => INTERVAL '1 hour');