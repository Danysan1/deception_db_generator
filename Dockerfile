ARG POSTGRES_VERSION=16.1-alpine
FROM postgres:${POSTGRES_VERSION}

COPY initdb.d/* /docker-entrypoint-initdb.d/

