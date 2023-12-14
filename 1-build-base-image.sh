#!/bin/sh
set -e

# Use the schema.sql file if it exists, otherwise use the default_Schema.sql file
rm -r initdb.d/*
[ -f schema.sql ] && cp schema.sql ./initdb.d/schema.sql || cp default_schema.sql ./initdb.d/schema.sql

# Build the Docker image for the DB
docker-compose build postgres-base
