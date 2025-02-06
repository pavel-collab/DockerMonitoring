-- Создаем основную таблицу
CREATE TABLE container_info (id SERIAL PRIMARY KEY, 
                             container_id TEXT NOT NULL, 
                             memory_limit DOUBLE PRECISION, 
                             status TEXT NOT NULL DEFAULT 'died');

-- создадим таблицу со статистикой
CREATE TABLE container_statistics(id INTEGER, 
                                  time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                  cpu_usage DOUBLE PRECISION,
                                  memory_usage DOUBLE PRECISION,
                                  kernel_cpu_usage DOUBLE PRECISION, 
                                  user_cpu_usage DOUBLE PRECISION, 
                                  system_cpu_usage DOUBLE PRECISION);

-- добавим этой таблице внещний ключ
ALTER TABLE container_detailed_statistics 
    ADD CONSTRAINT table_id FOREIGN KEY (id) REFERENCES container_info(id) ON DELETE CASCADE;

-- Превращаем ее в гипертаблицу
SELECT create_hypertable('container_statistics', 'time');

-- создадим таблицу с названиями сетевых соединений
CREATE TABLE networks (id SERIAL PRIMARY KEY, 
                       name TEXT NOT NULL);

-- создадим таблицу с сетевыми соединениями контейнеров
CREATE TABLE container_networks (container_id INTEGER,
                                 network_id INTEGER,
                                 time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                 resieved_bytes DOUBLE PRECISION,
                                 transmited_bytes DOUBLE PRECISION);

SELECT create_hypertable('container_networks', 'time');

-- добавим к этой таблице внешние ключи
ALTER TABLE container_networks 
    ADD CONSTRAINT container_id FOREIGN KEY (container_id) REFERENCES container_info(id) ON DELETE CASCADE;

ALTER TABLE container_networks 
    ADD CONSTRAINT network_id FOREIGN KEY (network_id) REFERENCES networks(id) ON DELETE CASCADE;