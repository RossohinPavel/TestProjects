FROM python:3.12.4-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
