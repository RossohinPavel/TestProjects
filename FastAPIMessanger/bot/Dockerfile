FROM python:3.12.4-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD python main.py
