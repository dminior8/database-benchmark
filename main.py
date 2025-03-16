import psycopg2
import pymongo
from cassandra.cluster import Cluster
import oracledb
import time

# Konfiguracja połączeń do baz danych
DB_CONFIG = {
    "postgres": {
        "host": "localhost",
        "port": 5432,
        "database": "postgres-test",
        "user": "postgres",
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
        "dsn": "localhost:1521/XE",
        "user": "system",
        "password": "YourPassword123"
    }
}

def check_postgres():
    try:
        print("Próba połączenia z PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG["postgres"])
        conn.set_client_encoding('LATIN1')
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
        conn = oracledb.connect(**DB_CONFIG["oracle"])
        conn.close()
        print("OracleDB is running!")
    except Exception as e:
        print("OracleDB connection failed:", e)

if __name__ == "__main__":
    print("Sprawdzanie statusu baz danych...")
    time.sleep(5)  # Czekamy, aby dać kontenerom czas na uruchomienie
    check_postgres()
    check_mongo()
    check_cassandra()
    check_oracle()
