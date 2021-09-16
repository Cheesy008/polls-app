#!/bin/sh

echo "Run migrations"
python3 manage.py migrate

echo "Start server"
python3 manage.py runserver 0.0.0.0:8000
