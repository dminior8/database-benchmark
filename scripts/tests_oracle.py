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

# Lista testów: liczba operacji CRUD
TEST_CASES = [1_000_000, 2_000_000, 5_000_000, 10_000_000]

def single_test(num_operations):
    """ Wykonuje test CRUD dla podanej liczby operacji """
    try:
        conn = oracledb.connect(
            user=DB_CONFIG["oracle"]["user"],
            password=DB_CONFIG["oracle"]["password"],
            dsn=DB_CONFIG["oracle"]["dsn"],
            mode=DB_CONFIG["oracle"]["mode"]
        )
        cursor = conn.cursor()

        total_create, total_read, total_update, total_delete = 0, 0, 0, 0

        print(f"\n🔄 Test dla {num_operations:,} operacji CRUD...")
        for i in range(num_operations):
            if i % (num_operations // 10) == 0:
                print(f"Postęp: {i:,}/{num_operations:,} operacji")

            # CREATE
            start_time = time.time()
            cursor.execute("""
                INSERT INTO users (user_id, first_name, last_name, phone, email, pesel, gender)
                VALUES (users_seq.NEXTVAL, 'John', 'Doe', '123456789', 'john.doe@example.com', '12345678901', 'male')
            """)
            conn.commit()
            total_create += time.time() - start_time

            # READ
            start_time = time.time()
            cursor.execute("SELECT * FROM users WHERE first_name = 'John' AND last_name = 'Doe'")
            cursor.fetchone()
            total_read += time.time() - start_time

            # UPDATE
            start_time = time.time()
            cursor.execute("""
                UPDATE users
                SET first_name = 'Jane'
                WHERE first_name = 'John' AND last_name = 'Doe'
            """)
            conn.commit()
            total_update += time.time() - start_time

            # DELETE
            start_time = time.time()
            cursor.execute("""
                DELETE FROM users
                WHERE first_name = 'Jane' AND last_name = 'Doe'
            """)
            conn.commit()
            total_delete += time.time() - start_time

        cursor.close()
        conn.close()

        # Podsumowanie
        print("\n📊 *** PODSUMOWANIE ***")
        print(f"🔹 {num_operations:,} operacji CREATE: {total_create:.2f} s (średnio {total_create / num_operations:.6f} s/op)")
        print(f"🔹 {num_operations:,} operacji READ: {total_read:.2f} s (średnio {total_read / num_operations:.6f} s/op)")
        print(f"🔹 {num_operations:,} operacji UPDATE: {total_update:.2f} s (średnio {total_update / num_operations:.6f} s/op)")
        print(f"🔹 {num_operations:,} operacji DELETE: {total_delete:.2f} s (średnio {total_delete / num_operations:.6f} s/op)")

    except Exception as e:
        print("Oracle CRUD Test failed:", e)

def crud_oracle():
    for test_case in TEST_CASES:
        single_test(test_case)
