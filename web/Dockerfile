FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

# Cache deps
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

#CMD python3 manage.py migrate; python3 -m gunicorn onlyVels.asgi:application -k uvicorn.workers.UvicornWorker -b :8080
