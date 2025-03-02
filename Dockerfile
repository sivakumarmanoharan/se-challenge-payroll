FROM python:3.12-slim

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app
COPY requirements.txt .
COPY alembic.ini /app/
COPY alembic /app/alembic
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

