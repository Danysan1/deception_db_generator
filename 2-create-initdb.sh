#!/bin/sh
set -e

# Stop and remove the DB container and its data volume
docker-compose --profile base down -v

# Start the DB
docker-compose --profile base --profile dev up -d
sleep 10

echo 'Filling the DB with fake realistic data...'
python create-initdb.py "postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_DB:-postgres}@localhost:5433/${POSTGRES_DB:-postgres}"

echo 'Dumping the DB data...'
docker-compose exec postgres-base pg_dump -U "${POSTGRES_USER:-postgres}" --dbname "${POSTGRES_DB:-postgres}" --blobs --section=pre-data --section=data --section=post-data --verbose | gzip > initdb.sql.gz
