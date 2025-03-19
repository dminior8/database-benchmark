FROM postgres:latest

ENV POSTGRES_DB=healthcare-postgres
ENV POSTGRES_USER=healthcare
ENV POSTGRES_PASSWORD=root

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432


