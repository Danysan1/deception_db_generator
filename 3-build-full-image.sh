#!/bin/sh
set -e

# Use the schema.sql file if it exists, otherwise use the default_Schema.sql file
rm -r initdb.d/*
[ -f initdb.sql.gz ] && cp initdb.sql.gz ./initdb.d/initdb.sql.gz || cp default_initdb.sql.gz ./initdb.d/initdb.sql.gz

# Build the Docker image for the DB
# The OUT_IMAGE_NAME environment variable MUST be specified
# Example: OUT_IMAGE_NAME=registry.gitlab.com/dsantini/deception-db-generator ./3-build-full-image.sh
#docker-compose build postgres-full
docker buildx bake postgres-full --pull --push
