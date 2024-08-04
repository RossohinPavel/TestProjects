FROM python:3.12.4-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn main:app --reload --host=0.0.0.0
