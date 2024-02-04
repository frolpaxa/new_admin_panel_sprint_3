#!/usr/bin/env bash

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

while ! nc -z $ES_HOST $ES_PORT; do
  sleep 0.1
done

curl -XPUT $ES_URL"movies" -H 'Content-Type: application/json' -d @es_schema.json

python main.py
