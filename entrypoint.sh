#!/bin/sh
set -e

# Wait until the database is ready
until pg_isready -h db -p 5432; do
    echo "Waiting for the database..."
    sleep 2
done

echo "Running migrations..."
alembic upgrade head

echo "Starting the application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
