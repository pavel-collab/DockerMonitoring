# Сборка и настройка СУБД PostgreSQL

Важнейшим этапом подготовки приложения к запуску является установка и настройка СУБД. Будем устанавливать стабильную версию PostgreSQL 
из исходного кода.

## Сборка и запуск СУБД

### Проверка зависимостей и скачивание исходного кода
```
# устанавливаем необходимые зависимости
sudo apt install -y gcc cmake make libssl-dev pkg-config libreadline-dev zlib1g-dev icu-devtools libicu-dev flex bison

# скачиваем исходный код СУБД и переключаемся на стабильную версию
RUN git clone https://github.com/postgres/postgres.git
cd postgresql
git checkout REL_16_6
```

### Сборка СУБД

```
./configure --prefix=/usr/local/lib/postgresql/16/ --libdir=/usr/local/lib/postgresql/16/lib/ --with-openssl
make
sudo make install
```

Создаем пользователя и дериктории под кластер
```
sudo useradd postgres -d /var/local/lib/postgresql/ -s /bin/bash
sudo mkdir -p /var/local/lib/postgresql/16/main/
sudo chown -R postgres:postgres /var/local/lib/postgresql/
```

Переключаемся на нового пользователя
```
sudo su - postgres

echo "export PGDATA=/var/local/lib/postgresql/16/main/" >> .bash_profile
echo "PATH=/usr/local/lib/postgresql/16/bin/:$PATH" >> .bash_profile
source .bash_profile
```

Создаем новый кластер.
```
pg_ctl initdb
```

### Настройка кластера

В конфигурационном файле postgresql.conf выставляем следующие параметры
```
listen_addresses = '*'
log_timezone = 'Europe/Moscow'

# настройка логирования
logging_collector = on
log_directory = ... # укажите удобную вам дерикторию
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
```

В конфигурационном файле pg_hba.conf добавляем строчку
```
host all all 0.0.0.0/0 trust
```

Это позволит подключаться к кластеру с различных хостов.

### Запуск сервера и создание базы

Запускаем сервер
```
pg_ctl start
```

Подключаемся к кластеру и создаем базу данных для работы приложения
```
psql -h localhost -p 5432 -U postgres -d postgres

CREATE DATABASE containers;
```