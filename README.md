# README

Небольшая программа для мониторинга статистики докер-контейнеров, создана в рамках изучения питоновского модуля docker, а так же 
расширения timescaleDB СУБД PostgreSQL.

### Настройка СУБД

```
pg_ctl initdb
```

Настраиваем postgresql.conf, выставляем следующие параметры:
```
# прослушиваемые адреса, чтобы принимать соединение
listen_addresses = '*'

# список динамически-загружаемых библиотек, чтобы работать с расширением
shared_preload_libraries = 'timescaledb'

# временная зона, чтобы временные метки были корректными
log_timezone = 'Europe/Moscow'
```

Настраиваем логирование
```
logging_collector = on
log_directory = ...
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
```

### Сорбка расширения TimescaleDB

### Подготовка расширения СУБД

Убедитесь, что ваша версия СУБД собрана с openssl, так как он требуется для работы timescaleDB. При необходимости пересоберите СУБД.

Также, убедитесь, что релизная версия СУБД и релизная версия расширения timescaleDB будут работать вместе, разные релизные версии timescaleDB могут работать не со
всеми версиями ядра. На момент написания инструкции timescaleDB вообще не умеет работать с версиями postgres 17 и выше. При тестировании автор использовал 
postgresql на релизной версии REL-16-4 и timescaleDB на релизной версии 2.17.2 (все собиралось из исходников)

Если вы планируете запускать postgresql на выделенном хосте, не забудьте поставить параметр
```
localhost = '*'
```
в конфигурационном файле postgresql.conf и настройку
```
host    all             all             0.0.0.0/0               trust
```
для доступа к базе через подключение со сторонних хостов.

### Сборка и подготовка timescaleDB

Подробную инструкцию по установке timescaleDB вы можете найти на их официальном гитхабе или в официальной документации. Перед запуском сервера не 
забудьте добавить расширение в postgresql.conf в секцию shared-preload-libraries.

### Создание гипертаблицы в базе данных

Запустите сервер и подключитесь к базе данных через command prompt на хосте с базой. Создайте расширение, убедитесь, что расширение создано корректно
```
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
```

Создайте гипертаблицу для хранения данных, для этого можно использовать
заготовленный скрипт
```
\ir ./create_table.sql
```
или просто выполнить все команды самостоятельно.

### Настройка непрерывных агрегатов и сжатия

```
create materialized view container_aggregation with (timescaledb.continuous) as select container_id as container, time_bucket('1 hour', time) as bucket, first(cpu_usage, time) as fst_cpu_usg, last(cpu_usage, time) as lst_cpu_usg, avg(cpu_usage) as avg_cpu_usg, first(memory_usage, time) as fst_mem_usg, last(memory_usage, time) as lst_mem_usg, avg(memory_usage) as avg_mem_usg from container_stats group by container_id, bucket;

select add_continuous_aggregate_policy('container_aggregation', start_offset => INTERVAL '3 hours', end_offset => INTERVAL '1 hour', schedule_interval => INTERVAL '1 hour');
```

```
alter table container_stats set (timescaledb.compress, timescaledb.compress_orderby='time', timescaledb.compress_segmentby = 'container_id');
```

### Запуск мониторинга

В питоновском скрипте пропишите необходимые праметры подключения и запустите скрипт.
