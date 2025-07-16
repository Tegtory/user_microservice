from python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --use-feature=fast-deps -r requirements.txt

COPY . .

CMD ["python", "-m", "user"]