# task.py
from celery import Celery
import redis

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
app = Celery('task', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)

@app.task
def add(x, y):
  return x + y

# celery -A task worker --loglevel=info --autoscale=3