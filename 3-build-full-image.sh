#!/bin/sh
set -e

# Use the schema.sql file if it exists, otherwise use the default_Schema.sql file
rm -r initdb.d/*
[ -f initdb.sql.gz ] && cp initdb.sql.gz ./initdb.d/initdb.sql.gz || cp default_initdb.sql.gz ./initdb.d/initdb.sql.gz

# Build the Docker image for the DB
docker-compose --profile full build
#docker buildx bake postgres --pull
