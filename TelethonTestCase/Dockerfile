FROM python:3.12.3-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app



COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY django .
COPY start.sh .
RUN chmod +x start.sh

CMD [ "./start.sh" ]
EXPOSE 8000