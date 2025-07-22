FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install poetry

COPY . .

RUN poetry install
RUN poetry run alembic upgrade head

ENTRYPOINT ["python", "-m", "user"]