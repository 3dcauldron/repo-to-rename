web: gunicorn djangoDocker.wsgi --limit-request-line 8188 --log-file -
worker: celery worker --app=djangoDocker --loglevel=info
