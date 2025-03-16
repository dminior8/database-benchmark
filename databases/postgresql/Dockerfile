FROM postgres:latest

ENV POSTGRES_DB=postgres-test
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=root

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
