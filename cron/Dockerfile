FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy

RUN apt-get update
RUN apt-get install tesseract-ocr -y

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD celery -A main worker --loglevel=INFO -B --concurrency=1
