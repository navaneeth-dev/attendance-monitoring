from celery import Celery

app = Celery('attendance', broker='redis://localhost')
app.conf.broker_connection_retry_on_startup = False

@app.task
def add(x, y):
    return x + y
