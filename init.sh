#!/bin/bash

set -e
psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "netflixdemo" <<-EOSQL
  CREATE USER postgres WITH PASSWORD 'postgres';
  CREATE DATABASE netflixdemo;
  GRANT ALL PRIVILEGES ON DATABASE netflixdemo TO postgres;
EOSQL

# Apply database migrations
echo "Initiate database migrations"
python src/manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python src/manage.py migrate

# Start server
echo "Starting server"
python src/manage.py runserver 0.0.0.0:8000