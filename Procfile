web: gunicorn wsgi:app 
worker: celery --app=tasks.app worker --loglevel=info