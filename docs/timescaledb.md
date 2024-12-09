# Установка и настройка расширения TimescaleDB для работы с временными рядами

## Сборка и установка расширения

Скачиваем исходный код расширения с официального сайта, переключаемся на релизную версию и собираем.
```
git clone https://github.com/timescale/timescaledb.git
cd timescaledb
git checkout 2.17.2
./bootstrap
cd build
make
sudo make install
```

Открываем конфигурационный файл базы данных PostgreSQL postgresql.conf и добавляем timescaledb к списку shared_preload_libraries:
```
shared_preload_libraries = 'timescaledb'
```

Сохраняем конфигурационный файл и перезапускаем кластер:
```
pg_ctl restart
```

Подключаемся к серверу к нужной базе и добавляем расширение
```
psql -h localhost -p 5432 -U postgres -d containers
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

## Создание гипертаблиц и настройка агрегатов

Для начала создадим основную таблицу для наших данных и превратим ее в гипертаблицу средствами расширения TimescaleDB
```
CREATE TABLE container_stats (
    container_id TEXT,
    cpu_usage DOUBLE PRECISION,
    memory_usage DOUBLE PRECISION,
    time TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

SELECT create_hypertable('container_stats', 'time');
```

Настроим непрерывные агрегаты. Непрерывные агрегаты имеют преимущество над обычными MATERIALIZED VIEW, так как обновляются автоматически без
исполнения дополнительных команд.
```
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
```

## Настройка автоматической компрессии

Расширение TimescaleDB позволяет настроить автоматическую компрессию данных.
```
ALTER TABLE container_stats 
    SET (timescaledb.compress, 
         timescaledb.compress_orderby='time', 
         timescaledb.compress_segmentby = 'container_id');
```

## Создание дополнительных таблиц

Таблица для общей информации по контейнерам. Содержит имя контейнера, соответствующий id и ограничение по памяти.
```
-- Создаем тмаблицу
CREATE TABLE container_info (id TEXT NOT NULL, 
                             name TEXT, 
                             memory_limit DOUBLE PRECISION);

-- Создаем первычный ключ в этой таблийе (она будет основной, все остальные таблицы будут ссылаться на нее)
ALTER TABLE container_info ADD CONSTRAINT container_id PRIMARY KEY (id);
```

Более детальная статистика по занятовсти CPU. Содержит время, занимаемое на CPU в kernel, user и system состояниях.
```
-- заводим таблицу
CREATE TABLE container_detailed_statistics (id TEXT, 
                                            time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                            kernel_cpu_usage DOUBLE PRECISION, 
                                            user_cpu_usage DOUBLE PRECISION, 
                                            system_cpu_usage DOUBLE PRECISION);

-- Превращаем ее в гипертаблицу
SELECT create_hypertable('container_detailed_statistics', 'time');

-- Добавляем внешний ключ на основную таблицу
ALTER TABLE container_detailed_statistics 
    ADD CONSTRAINT container_id FOREIGN KEY (id) REFERENCES container_info(id) ON DELETE CASCADE;

-- Настраиваем сжатие данных
ALTER TABLE container_detailed_statistics 
    SET (timescaledb.compress, 
         timescaledb.compress_orderby='time', 
         timescaledb.compress_segmentby = 'id');
```

Статистика по сетевым соединениям контейнеров.
```
-- Создаем тмаблицу
CREATE TABLE container_networks (id TEXT,
                                 time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                 network_name TEXT,
                                 resieved_bytes DOUBLE PRECISION,
                                 transmited_bytes DOUBLE PRECISION);

-- Превращаем ее в гипертаблицу
SELECT create_hypertable('container_networks', 'time');

-- Добавляем внешний ключ на основную таблицу
ALTER TABLE container_networks 
    ADD CONSTRAINT container_id FOREIGN KEY (id) REFERENCES container_info(id) ON DELETE CASCADE;

-- Настраиваем сжатие данных
ALTER TABLE container_networks 
    SET (timescaledb.compress, 
         timescaledb.compress_orderby='time', 
         timescaledb.compress_segmentby = 'id');
```