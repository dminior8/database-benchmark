FROM container-registry.oracle.com/database/enterprise:19.3.0

#Set CDB name
ENV ORACLE_SID=ORCLCDB

#Set PDB name
ENV ORACLE_PWD=YourPassword123

COPY init.sql /docker-entrypoint-initdb.d/
COPY scripts /opt/oracle/scripts


EXPOSE 1521 5500
