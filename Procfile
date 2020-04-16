release: python manage.py migrate
web: daphne -b 0.0.0.0 -p $PORT api.asgi:application
celery: REMAP_SIGTERM=SIGQUIT celery -A api worker -l info -B
