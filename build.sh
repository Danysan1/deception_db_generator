#!/bin/sh
cd $(dirname "$0")
docker buildx bake postgres --pull --push
