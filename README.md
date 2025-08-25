# Tegtory User Microservice

this microservice work with bots to manage users and their data, storing data like ban status and providing user-related services.

## Features

- User registration and authentication
- Notifications about user registration ( disabled by default )

## Start up

### environment variables

- `DB_HOST`: URL of the database to connect to.
- `DB_PORT`: Database port. default: 5432
- `DB_NAME`: Database name.
- `DB_USER`: Database username.
- `DB_PASSWORD`: Database password.
- `SECRET_KEY`: Secret key for authorizing services.

`for rabbitmq environments check user/common/config.py`

### Docker

```bash
$ docker compose -f docker/docker-compose.dev.yml --env-file .env up -d --build
```

### python

```bash
pip install poetry # if not installed
poetry install
poetry run python -m user
```

# TODO

- [ ] Implement profile actions
- [ ] mTLS??

# contribution

any contributions are welcome, please open an issue or a pull request.

