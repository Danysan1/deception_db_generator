#!/bin/sh
set -e

# Stop and remove the DB container and its data volume
docker-compose --profile base down -v

docker-compose --profile full up -d
