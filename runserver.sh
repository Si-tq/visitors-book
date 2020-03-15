#!/bin/bash

echo "${0}: [1] Applying migrations..."
python manage.py migrate

echo "${0}: creating admin user."
echo "from django.contrib.auth.models import User; print(\"Admin exists\") if User.objects.filter(username='admin').exists() else User.objects.create_superuser('admin', 'admin@admin.pl', 'admin')" | python manage.py shell

echo "${0}: [2] Collecting static files..."
python manage.py collectstatic --noinput

echo "${0}: [3] Running server..."
python manage.py runserver

