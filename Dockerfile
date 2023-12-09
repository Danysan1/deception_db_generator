# https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-9193 & https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-10164
ARG POSTGRES_VERSION=11.2 

FROM postgres:${POSTGRES_VERSION}

COPY ./initdb.d/* /docker-entrypoint-initdb.d/

