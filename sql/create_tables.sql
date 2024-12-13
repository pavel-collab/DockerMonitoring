-- Создаем основную таблицу таблицу
CREATE TABLE container_info (id TEXT NOT NULL,
	                     name TEXT,
		             memory_limit DOUBLE PRECISION);

-- Заводим таблицу со статистикой
CREATE TABLE container_stats (container_id TEXT,
	                      cpu_usage DOUBLE PRECISION,
	                      memory_usage DOUBLE PRECISION,
	                      time TIMESTAMPTZ NOT NULL DEFAULT NOW());

-- Превращаем ее в гипертаблицу
SELECT create_hypertable('container_stats', 'time');

-- Заводим таблицу с более детальной статистикой
CREATE TABLE container_detailed_statistics (id TEXT,
	                                    time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
			                    kernel_cpu_usage DOUBLE PRECISION,
                                            user_cpu_usage DOUBLE PRECISION,
					    system_cpu_usage DOUBLE PRECISION);


-- Превращаем ее в гипертаблицу
SELECT create_hypertable('container_detailed_statistics', 'time');

-- Создаем таблицу для информации по сетевым соединениям
CREATE TABLE container_networks (id TEXT,
	                         time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
			         network_name TEXT,
				 resieved_bytes DOUBLE PRECISION,
		                 transmited_bytes DOUBLE PRECISION);

-- Превращаем ее в гипертаблицу
SELECT create_hypertable('container_networks', 'time');


