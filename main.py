import psycopg2
import pymongo
from cassandra.cluster import Cluster
import oracledb

from databases.mongo.data_generator import generate_and_insert_data_mongo
from databases.oracle.data_generator import generate_and_insert_data_oracle
from databases.postgresql.data_generator import generate_and_insert_data_postgres
from databases.cassandra.data_generator import generate_and_insert_data_cassandra

from scripts.tests_mongo import crud_mongo
from scripts.tests_oracle import crud_oracle
from scripts.tests_postgresql import crud_postgres
from scripts.tests_cassandra import crud_cassandra

DB_CONFIG = {
    "postgres": {
        "host": "localhost",
        "port": 5432,
        "database": "healthcare-postgres",
        "user": "healthcare",
        "password": "root"
    },
    "mongo": {
        "host": "localhost",
        "port": 27017,
        "username": "root",
        "password": "example"
    },
    "cassandra": {
        "host": "localhost",
        "port": 9042
    },
    "oracle": {
        "dsn": "localhost:1521/XEPDB1",  # Upewnij się, że to jest poprawny DSN
        "user": "SYS",
        "password": "YourPassword123",
        "mode": oracledb.SYSDBA  # Tutaj ustawiamy tryb SYSDBA
    }
}

def check_postgres():
    try:
        conn = psycopg2.connect(#database="postgres", user="postgres", password="admin")
            # **DB_CONFIG
            database="healthcare-postgres",
            user="healthcare",
            password="root",
            host="localhost",
            port = 5433
        )


        # conn.set_client_encoding('UTF8')
        conn.close()
        print("PostgreSQL is running!")
    except Exception as e:
        print("PostgreSQL connection failed:", e)

def check_mongo():
    try:
        client = pymongo.MongoClient(**DB_CONFIG["mongo"])
        client.server_info()  # Test połączenia
        print("MongoDB is running!")
    except Exception as e:
        print("MongoDB connection failed:", e)

def check_cassandra():
    try:
        cluster = Cluster([DB_CONFIG["cassandra"]["host"]])
        cluster.connect()
        print("CassandraDB is running!")
    except Exception as e:
        print("Cassandra connection failed:", e)

def check_oracle():
    try:
        conn = oracledb.connect(
            user=DB_CONFIG["oracle"]["user"],
            password=DB_CONFIG["oracle"]["password"],
            dsn=DB_CONFIG["oracle"]["dsn"],
            mode=oracledb.SYSDBA
        )
        conn.close()
        print("OracleDB is running!")
    except Exception as e:
        print("OracleDB connection failed:", e)

if __name__ == "__main__":
    print("Checking database status...")
    #time.sleep(10)  # Czekamy, aby dać kontenerom czas na uruchomienie
    check_postgres()
    check_mongo()
    check_cassandra()
    check_oracle()

    print("\n\nGenerating and adding data to the database...")
    generate_and_insert_data_postgres()
    generate_and_insert_data_mongo()
    generate_and_insert_data_oracle()
    generate_and_insert_data_cassandra()


    print("\n\nStarting test...")

    print("\nRunning CRUD tests for Oracle...")
    crud_oracle()

    print("\nRunning CRUD tests for Cassandra...")
    crud_cassandra()

    print("\nRunning CRUD tests for MongoDB...")
    crud_mongo()

    print("\nRunning CRUD tests for PostgreSQL...")
    crud_postgres()