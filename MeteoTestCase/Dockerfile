FROM python:3.12.3-slim

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "./start.sh" ]
