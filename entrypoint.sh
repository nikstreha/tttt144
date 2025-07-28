#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

flask db upgrade
exec gunicorn --bind 0.0.0.0:8000 -w 4 -k gthread --threads 2 app:app