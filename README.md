# warehouse

# Инструкция по запуску приложения

1. В папку `app` добавить файл `.env` со следующими параметрами
```
DB_HOST=postgres
DB_PORT=5432
DB_NAME=warehouse
DB_USER=admin
DB_PASS=admin
```

2. Далее из корневой папки проекта `warehouse` выполнить команду `docker compose up --build`
___
# Документация

После запуска приложения документация в виде swagger доступна по [ссылке](http://localhost:8000/docs)
___

# Работа с БД

1. В терминале выполняем команду `docker exec -it db /bin/sh`
2. Затем подключаемся к БД по команде `psql -d warehouse -U admin`
3. Добавляем статусы для заказов
```sql
insert into order_statuses
(name)
values
('в процессе'),
('отправлен'),
('доставлен');
```
---


# Тестирование

1. Перейти в директорию `pg_db_for_tests`
2. В терминале выполнить команду `docker compose up --build`
3. Из корневой папки в терминале выполнить команду `pytest -v tests/`