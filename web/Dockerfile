FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD python3 manage.py migrate; python3 -m gunicorn onlyVels.asgi:application -k uvicorn.workers.UvicornWorker -b :8080
