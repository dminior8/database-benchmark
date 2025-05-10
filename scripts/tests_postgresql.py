import psycopg2
import time

DB_CONFIG = {
    "postgres": {
        "host": "localhost",
        "port": 5433,
        "database": "healthcare-postgres",
        "user": "healthcare",
        "password": "root"
    }
}

TEST_CASES = [100, 200, 300, 500, 1_000, 5_000, 10_000, 15_000, 20_000]


def crud_postgres():
    create_times = []
    read_times = []
    update_times = []
    delete_times = []

    for n in TEST_CASES:
        conn = psycopg2.connect(**DB_CONFIG["postgres"])
        cur = conn.cursor()

        # CREATE
        start = time.time()
        for _ in range(n):
            cur.execute(
                "INSERT INTO users (first_name, last_name, phone, email, pesel) "
                "VALUES ('John','Doe','123456789','johndoe@example.com','12345678901');"
            )
        conn.commit()
        create_times.append(time.time() - start)

        # READ
        start = time.time()
        for _ in range(n):
            cur.execute("SELECT * FROM users WHERE first_name = 'John' AND last_name = 'Doe';")
            cur.fetchone()
        read_times.append(time.time() - start)

        # UPDATE
        start = time.time()
        for _ in range(n):
            cur.execute("UPDATE users SET first_name = 'Jane' WHERE first_name = 'John' AND last_name = 'Doe';")
        conn.commit()
        update_times.append(time.time() - start)

        # DELETE
        start = time.time()
        for _ in range(n):
            cur.execute("DELETE FROM users WHERE first_name = 'Jane' AND last_name = 'Doe';")
        conn.commit()
        delete_times.append(time.time() - start)

        cur.close()
        conn.close()

    return [
        TEST_CASES,
        create_times,
        read_times,
        update_times,
        delete_times,
        "PostgreSQL",
        "red"
    ]
