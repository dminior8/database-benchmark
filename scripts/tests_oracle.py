import oracledb
import time

# Konfiguracja połączenia z Oracle
DB_CONFIG = {
    "oracle": {
        "dsn": "localhost:1521/XE",
        "user": "SYS",
        "password": "YourPassword123",
        "mode": oracledb.SYSDBA
    }
}

TEST_CASES = [100, 200, 300, 500, 1_000, 5_000, 10_000, 15_000, 20_000]


def single_test_oracle(num_operations):
    """
    Wykonuje num_operations operacji CRUD na Oracle i zwraca czasy w formacie:
    [ TEST_CASES, create_times, read_times, update_times, delete_times, label, color ]
    """
    conn = oracledb.connect(
        user=DB_CONFIG["oracle"]["user"],
        password=DB_CONFIG["oracle"]["password"],
        dsn=DB_CONFIG["oracle"]["dsn"],
        mode=DB_CONFIG["oracle"]["mode"]
    )
    cursor = conn.cursor()

    # Zerujemy sumy czasów
    total_create = total_read = total_update = total_delete = 0.0

    # CREATE
    start = time.time()
    for _ in range(num_operations):
        cursor.execute("""
            INSERT INTO users (
                user_id, first_name, last_name,
                phone, email, pesel, gender
            ) VALUES (
                users_seq.NEXTVAL, 'John', 'Doe',
                '123456789', 'john.doe@example.com',
                '12345678901', 'male'
            )
        """)
    conn.commit()
    total_create = time.time() - start

    # READ
    start = time.time()
    for _ in range(num_operations):
        cursor.execute("""
            SELECT * FROM users
            WHERE first_name = 'John' AND last_name = 'Doe'
        """)
        cursor.fetchone()
    total_read = time.time() - start

    # UPDATE
    start = time.time()
    for _ in range(num_operations):
        cursor.execute("""
            UPDATE users
            SET first_name = 'Jane'
            WHERE first_name = 'John' AND last_name = 'Doe'
        """)
    conn.commit()
    total_update = time.time() - start

    # DELETE
    start = time.time()
    for _ in range(num_operations):
        cursor.execute("""
            DELETE FROM users
            WHERE first_name = 'Jane' AND last_name = 'Doe'
        """)
    conn.commit()
    total_delete = time.time() - start

    cursor.close()
    conn.close()

    # Zwracamy jedną serię dla Oracle
    return [
        TEST_CASES,
        total_create,
        total_read,
        total_update,
        total_delete,
        "Oracle",
        "blue"
    ]


def crud_oracle():
    """
    Dla każdego n w TEST_CASES wywołuje single_test_oracle(n),
    a potem zwraca listę czterech list czasów + etykietę i kolor.
    """
    create_times = []
    read_times = []
    update_times = []
    delete_times = []

    for n in TEST_CASES:
        row = single_test_oracle(n)
        # row = [TEST_CASES, c, r, u, d, "Oracle", "blue"]
        _, c, r, u, d, _, _ = row
        create_times.append(c)
        read_times.append(r)
        update_times.append(u)
        delete_times.append(d)

    return [
        TEST_CASES,
        create_times,
        read_times,
        update_times,
        delete_times,
        "Oracle",
        "blue"
    ]
