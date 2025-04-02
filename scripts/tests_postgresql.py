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

def crud_postgres():
    try:
        # Połączenie z bazą danych PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG["postgres"])
        cursor = conn.cursor()

        # CREATE
        start_time = time.time()
        cursor.execute("INSERT INTO users (first_name, last_name, phone, email, pesel) VALUES ('John', 'Doe', '123456789', 'johndoe@example.com', '12345678901');")
        conn.commit()
        print("PostgreSQL CREATE Time:", time.time() - start_time)

        # READ
        start_time = time.time()
        cursor.execute("SELECT * FROM users LIMIT 1;")
        cursor.fetchone()
        print("PostgreSQL READ Time:", time.time() - start_time)

        # UPDATE
        start_time = time.time()
        cursor.execute("UPDATE users SET first_name = 'Updated' WHERE first_name = 'John';")
        conn.commit()
        print("PostgreSQL UPDATE Time:", time.time() - start_time)

        # DELETE
        start_time = time.time()
        cursor.execute("DELETE FROM users WHERE first_name = 'Updated';")
        conn.commit()
        print("PostgreSQL DELETE Time:", time.time() - start_time)

        # Zamykanie kursora i połączenia
        cursor.close()
        conn.close()
    except Exception as e:
        print("PostgreSQL CRUD Test failed:", e)
