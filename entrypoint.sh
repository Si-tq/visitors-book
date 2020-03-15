#!/bin/sh

NAME="main"
SERVER="0.0.0.0:8000"
NUM_WORKERS=1
NUM_THREADS=3

set -e

echo "${0}: running migrations."
python manage.py migrate

echo "${0}: collecting statics."
python manage.py collectstatic --noinput

echo "${0}: creating admin user."
echo "from django.contrib.auth.models import User; print(\"Admin exists\") if User.objects.filter(username='$USER').exists() else User.objects.create_superuser('$USER', '$MAIL', '$PASSWORD')" | python manage.py shell

echo "${0}: running app."

gunicorn main.wsgi:application \
	--name=$NAME \
	--bind=$SERVER \
	--timeout=900 \
	--workers=$NUM_WORKERS \
	--threads=$NUM_THREADS \
	--worker-connections=1000 \
	--log-level=info \
	--reload \
	--reload-engine inotify

exec "$@"