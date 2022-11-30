import celery
from datetime import datetime

app = celery.Celery('example')
@app.task
def gettime():
    return datetime.now()