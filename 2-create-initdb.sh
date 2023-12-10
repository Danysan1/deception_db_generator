#!/bin/sh

# Start the DB
docker-compose --profile base up -d
sleep 10

# Fill the DB with fake realistic data
python create-initdb.py

# Dump the DB data
docker-compose exec postgres-base pg_dump -U "${POSTGRES_USER:-postgres}" --dbname "${POSTGRES_DB:-postgres}" --blobs --section=pre-data --section=data --section=post-data --verbose | gzip > initdb.sql.gz
