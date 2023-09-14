FROM postgres:14.2-alpine

ENV CONFIG_PATH configs/postgres

ARG POSTGRES_DB

COPY ${CONFIG_PATH}/psql_dump.sql /docker-entrypoint-initdb.d/
