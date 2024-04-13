web: gunicorn core.wsgi --log-file -
release: ./manage.py makemigrations && ./manage.py migrate && ./manage.py collectstatic --no-input
worker: celery -A core beat -l INFO