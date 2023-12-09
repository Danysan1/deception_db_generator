#!/bin/sh

# Use the schema.sql file if it exists, otherwise use the default_Schema.sql file
rm -r initdb.d/*
[ -f initdb.backup ] && cp initdb.backup ./initdb.d/initdb.backup

# Build the Docker image for the DB
[ -f .env.full ] || echo 'OUT_IMAGE_TAG=latest-full' > .env.full
docker-compose --env-file .env.full --profile db build
#docker buildx bake postgres --pull
