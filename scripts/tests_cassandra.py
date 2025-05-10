from cassandra.cluster import Cluster
import time
import uuid

DB_CONFIG = {
    "cassandra": {
        "host": "localhost",
        "port": 9042
    }
}

TEST_CASES = [100, 200, 300, 500, 1_000, 5_000, 10_000, 15_000, 20_000]

def crud_cassandra():
    """
    Dla każdej wartości w TEST_CASES wykonuje n operacji CRUD na Cassandra,
    mierzy czas i zwraca listę:
    [ TEST_CASES, create_times, read_times, update_times, delete_times, label, color ]
    """
    create_times = []
    read_times = []
    update_times = []
    delete_times = []

    # Połączenie z klastrem Cassandra i keyspace 'healthcare'
    cluster = Cluster([DB_CONFIG["cassandra"]["host"]])
    session = cluster.connect("healthcare")

    for n in TEST_CASES:
        # CREATE
        start = time.time()
        user_id = uuid.uuid4()
        for _ in range(n):
            session.execute(
                """
                INSERT INTO users (
                  user_id, first_name, last_name,
                  phone, email, birth_date, gender, pesel
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (user_id, 'John', 'Doe', '123456789',
                 'john.doe@example.com', '1990-01-01', 'male', '12345678901')
            )
        create_times.append(time.time() - start)

        # READ
        start = time.time()
        for _ in range(n):
            session.execute(
                "SELECT * FROM users WHERE user_id = %s",
                (user_id,)
            )
        read_times.append(time.time() - start)

        # UPDATE
        start = time.time()
        for _ in range(n):
            session.execute(
                """
                UPDATE users
                SET first_name = %s
                WHERE user_id = %s
                """,
                ('Jane', user_id)
            )
        update_times.append(time.time() - start)

        # DELETE
        start = time.time()
        for _ in range(n):
            session.execute(
                "DELETE FROM users WHERE user_id = %s",
                (user_id,)
            )
        delete_times.append(time.time() - start)

    # Zamknięcie połączenia
    session.shutdown()
    cluster.shutdown()

    return [
        TEST_CASES,
        create_times,
        read_times,
        update_times,
        delete_times,
        "Cassandra",
        "purple"
    ]
