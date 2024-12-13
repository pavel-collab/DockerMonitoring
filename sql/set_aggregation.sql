-- Добавляем непрерывные агрегаты и политику обновления
CREATE MATERIALIZED VIEW container_aggregation
    WITH (timescaledb.continuous) AS
        SELECT
	            container_id AS container,
		            time_bucket('1 hour', time) AS bucket,
			            first(cpu_usage, time) AS fst_cpu_usg,
				            last(cpu_usage, time) AS lst_cpu_usg,
					            avg(cpu_usage) AS avg_cpu_usg,
						            first(memory_usage, time) AS fst_mem_usg,
							            last(memory_usage, time) AS lst_mem_usg,
								            avg(memory_usage) AS avg_mem_usg
									        FROM container_stats
										        GROUP BY
											            container_id,
												            bucket;

													SELECT add_continuous_aggregate_policy('container_aggregation',
														                                        start_offset => INTERVAL '3 hours',
																			                                        end_offset => INTERVAL '1 hour',
																								                                        schedule_interval => INTERVAL '1 hour');
