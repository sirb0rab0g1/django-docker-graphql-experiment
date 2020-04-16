#!/bin/bash
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log

if [ "$ENV" = "production" ]; then
    ./manage.py migrate --no-input
    ./manage.py collectstatic --no-input
    ./manage.py create_admin
    ./manage.py create_aeon_devs
    ./manage.py create_statement_value
    daphne -b 0.0.0.0 -p $PORT api.asgi:application
else
    # ./manage.py migrate --no-input
    # ./manage.py collectstatic --no-input
    # ./manage.py create_admin
    # ./manage.py create_aeon_devs
    # ./manage.py create_statement_value
    echo "env dev"
    daphne -b 0.0.0.0 -p 8000 api.asgi:application
fi
# Prepare log files and start outputting logs to stdout
