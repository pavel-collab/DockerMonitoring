# README

## О продукте

Данная программа представляет собой систему мониторинга докер-контейнеров. Просто запустите эту программу на вашем хосте с контейнерами и вы
сможете отслеживать все запущенные докер-контейнеры, а также потребляемые ими ресурсы. Сколько памяти потребляет каждый контейнер, какие 
сетевые интерфейсы он использует, детальная информация по используемым ресурсам процессора. Все это доступно в удобном и понятном 
web-интерфейсе. Вы сможете получить информацию по разным временным промежуткам или за все время использования контейнеров, информацию об
отдельном контейнере или сравнительную статистику по группе контейнеров.

Приложение использует высокопроизводительную СУБД PostgreSQL и расширение TimescaleDB для оптимальной работы с временными рядами.

## Запуск демона

Для начала работы приложения убедитесь, что на вашем хосте установлены необходимые зависимости, их вы можете посмотреть в файле _requirements.txt_. 
Если у вас не хватает каких-либо зависимостей, вы можете их доустановить или создать для приложение отдельное виртуальное окружение:
```
python3 -m venv ./.venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

Перед запуском основной программы убедитесь, что у вас настроет сервер postgresql. Вы можете прочитать инструкции по установке и настройке
PostgreSQL и TimescaleDB в каталоге __docs__ или обратитесь к data base administrator вашей компании.
В конфигурационном файле _conf/connection.json_ заполните обязательные поля:
- _dbname_ -- имя вашей базы данных
- _host_ip_ -- ip-адрес вашего postgresql кластера (если кластер развернут на локальном хосте, можно указать _localhost_)

Если все зависимости установлены, вы можете просто запустить скрипт _main.py_ на том хосте, где зарущены ваши докер-контейнеры
```
python3 main.py
```

## Запуск web-интерфейса

После запуска мониторинга собранную статистику можно будет посмотреть в удобном и интуитивно-понятном web-интерфейсе. О том, как запустить
web-часть приложения и посмотреть статистику вы можете прочитать в _webapp/README.md_