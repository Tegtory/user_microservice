FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY . .

RUN poetry install

RUN poetry run python -m grpc_tools.protoc --proto_path=./protos/ --python_out=. --grpc_python_out=. protos/user/*.proto


CMD ["poetry", "run", "python", "-m", "user"]