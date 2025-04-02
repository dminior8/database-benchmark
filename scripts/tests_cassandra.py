from cassandra.cluster import Cluster
import time
import uuid

DB_CONFIG = {
    "cassandra": {
        "host": "localhost",
        "port": 9042
    }
}

def crud_cassandra():
    try:
        cluster = Cluster([DB_CONFIG["cassandra"]["host"]])
        session = cluster.connect("healthcare")  # Używamy keyspace 'healthcare'

        # CREATE
        start_time = time.time()
        user_id = uuid.uuid4()  # Generujemy UUID dla nowego użytkownika
        session.execute("""
            INSERT INTO users (user_id, first_name, last_name, phone, email, birth_date, gender, pesel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, 'John', 'Doe', '123456789', 'john.doe@example.com', '1990-01-01', 'male', '12345678901'))
        print("Cassandra CREATE Time:", time.time() - start_time)

        # READ
        start_time = time.time()
        rows = session.execute("""
            SELECT * FROM users WHERE user_id = %s
        """, (user_id,))
        for row in rows:
            print(row)
        print("Cassandra READ Time:", time.time() - start_time)

        # UPDATE
        start_time = time.time()
        session.execute("""
            UPDATE users
            SET first_name = %s
            WHERE user_id = %s
        """, ('Jane', user_id))
        print("Cassandra UPDATE Time:", time.time() - start_time)

        # DELETE
        start_time = time.time()
        session.execute("""
            DELETE FROM users WHERE user_id = %s
        """, (user_id,))
        print("Cassandra DELETE Time:", time.time() - start_time)

    except Exception as e:
        print("Cassandra CRUD Test failed:", e)

