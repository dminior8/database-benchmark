FROM container-registry.oracle.com/database/enterprise:19.3.0

ENV ORACLE_SID=ORCLCDB
ENV ORACLE_PDB=ORCLPDB1
ENV ORACLE_PWD=YourSecurePassword

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 1521 5500
