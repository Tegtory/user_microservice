FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install poetry

COPY . .
COPY .env .env

RUN poetry install

RUN poetry run python -m grpc_tools.protoc --proto_path=./protos/ --python_out=. --grpc_python_out=. protos/user/*.proto


CMD ["poetry", "run", "python", "-m", "user"]