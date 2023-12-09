#!/bin/sh

# Start the DB
docker-compose --profile db up -d
sleep 10

# Fill the DB with fake realistic data
python create-initdb.py

# Dump the DB data
docker-compose exec postgres pg_dump -U "${POSTGRES_USER:-postgres}" --dbname "${POSTGRES_DB:-postgres}" --format=c --verbose > initdb.backup
