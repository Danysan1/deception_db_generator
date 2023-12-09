#!/bin/sh

# Stop and remove the DB container and its data volume
docker-compose --profile db down -v
