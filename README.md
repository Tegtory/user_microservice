# Микросервис авторизации - Tegtory

## запуск

1. генерация .py файлов из протокола

    ```bash
   > .\compile_proto.bat
    ```

2. env

3. запуск

    ```bash
   > alembic upgrade head
    ```

    ```bash
   > python -m user
    ```

4. или дев/прод стенды

    ```bash
   > docker compose -f ...
    ```

# TODO

- [ ] Полноценная авторизация с помощью ТГ
- [ ] Оптимизация и улучшения уведомлений RabbitMQ
