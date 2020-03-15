#!/bin/sh

clear; find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

rm -rf ./.cache/ && \
rm -rf logs/ && \
rm -rf media/ && \
rm -rf *.png  && \
rm -rf .DS_Store && \
rm -rf nginx_logs/ && \
rm -rf htmlcov/ && \
rm -rf *.db && \
rm -rf .coverage && \
rm -rf celerybeat.pid && \
rm -rf db.sqlite3 && \
rm -rf ./static/admin && \
rm -rf ./static/django_extensions/ && \
rm -rf ./.pytest_cache/ && \
docker rm $(docker ps -a -q) -f && \
docker volume rm `docker volume ls -q -f dangling=true` && \
echo y |docker system prune && \
echo y | docker volume prune && \