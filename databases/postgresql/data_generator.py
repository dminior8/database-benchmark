import psycopg2
from faker import Faker
import random
import time

# Konfiguracja bazy danych
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "healthcare-postgres",
    "user": "healthcare",
    "password": "root"
}

DATA_CONFIG = {
    "num_users": 100,
    "num_doctors": 10,
    "num_clinics": 10,
    "num_examinations": 200,
    "num_user_basic_data": 100,  # Liczba użytkowników z podstawowymi danymi
    "num_medical_interviews": 100  # Liczba użytkowników z wywiadami medycznymi
}

def clear_database():
    """Usuwa dane z tabel przed dodaniem nowych."""
    conn = psycopg2.connect(
        database="healthcare-postgres",
        user="healthcare",
        password="root",
        host="localhost",  # Użyj localhost, bo port 5432 jest wystawiony na zewnątrz
        port=5433
    )
    # conn = psycopg2.connect(database="postgres", user="postgres", password="admin")
    cursor = conn.cursor()

    tables = [
        "short_medical_interviews",
        "users_basic_data",
        "examinations",
        "doctors_clinics",
        "doctors",
        "clinics",
        "users"
    ]

    for table in tables:
        # Sprawdzanie, czy tabela istnieje
        cursor.execute(f"""SELECT 1 FROM information_schema.tables WHERE table_name = '{table}';""")

        # Jeśli tabela istnieje, to usuwamy z niej dane
        if cursor.fetchone():
            cursor.execute(f"DELETE FROM {table};")

    conn.commit()
    cursor.close()
    conn.close()
    print("\nThe PostgreSQL database has been successfully cleared!")

def generate_users(cursor, fake, num_users):
    """Generuje użytkowników i zwraca ich ID."""
    user_ids = []

    for _ in range(num_users):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.phone_number()[:14]
        email = fake.unique.email()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
        gender = fake.random_element(elements=('male', 'female'))
        pesel = str(fake.random_int(min=10000000000, max=99999999999))

        cursor.execute("""
            INSERT INTO users (first_name, last_name, phone, email, birth_date, gender, pesel)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING user_id;
        """, (first_name, last_name, phone, email, birth_date, gender, pesel))

        user_id = cursor.fetchone()[0]
        user_ids.append(user_id)

    return user_ids

def generate_doctors(cursor, fake, num_doctors):
    """Generuje lekarzy i zwraca ich ID."""
    doctor_ids = []

    for _ in range(num_doctors):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.phone_number()[:14]
        email = fake.unique.email()
        gender = fake.random_element(elements=('male', 'female'))

        cursor.execute("""
            INSERT INTO doctors (first_name, last_name, phone, email, gender)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING doctor_id;
        """, (first_name, last_name, phone, email, gender))

        doctor_id = cursor.fetchone()[0]
        doctor_ids.append(doctor_id)

    return doctor_ids


def generate_clinics(cursor, fake, num_clinics):
    """Generuje przychodnie i zwraca ich ID."""
    clinic_ids = []

    for _ in range(num_clinics):
        name = fake.company()
        address = fake.address()
        phone = fake.phone_number()[:14]

        cursor.execute("""
            INSERT INTO clinics (name, address, phone)
            VALUES (%s, %s, %s)
            RETURNING clinic_id;
        """, (name, address, phone))

        clinic_id = cursor.fetchone()[0]  # Pobranie ID nowo dodanej kliniki
        clinic_ids.append(clinic_id)  # Dodanie do listy

    return clinic_ids


def generate_examinations(cursor, fake, users, doctors, num_examinations):
    """Generuje badania medyczne."""
    examinations_ids = []

    for _ in range(num_examinations):
        name = fake.word()
        exam_date = fake.date_this_decade().strftime('%Y-%m-%d')
        doctor_id = random.choice(doctors)
        user_id = random.choice(users)

        cursor.execute("""
            INSERT INTO examinations (name, examination_date, doctor_id, user_id)
            VALUES (%s, %s, %s, %s)
            RETURNING examination_id;
        """, (name, exam_date, doctor_id, user_id))

        examinations_id = cursor.fetchone()[0]  # Pobranie ID nowo dodanej kliniki
        examinations_ids.append(examinations_id)

    return examinations_ids

def generate_user_basic_data(cursor, fake, users, num_entries):
    """Generuje podstawowe dane dla określonej liczby użytkowników."""
    selected_users = random.sample(users, min(num_entries, len(users)))

    for user_id in selected_users:
        weight = round(random.uniform(50, 120), 2)
        height = random.randint(150, 200)
        systolic_pressure = random.randint(90, 140)
        diastolic_pressure = random.randint(60, 90)
        temperature = round(random.uniform(36.0, 39.0), 1)
        entry_date = fake.date_this_decade()

        cursor.execute("""
            INSERT INTO users_basic_data (user_id, weight, height, systolic_pressure, diastolic_pressure, temperature, entry_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (user_id, weight, height, systolic_pressure, diastolic_pressure, temperature, entry_date))

def generate_medical_interviews(cursor, fake, users, num_entries):
    """Generuje wywiady medyczne dla określonej liczby użytkowników."""
    selected_users = random.sample(users, min(num_entries, len(users)))

    for user_id in selected_users:
        symptoms = fake.random_element(elements=('pain', 'sticky', 'press', 'other'))
        temperature = round(random.uniform(36.0, 39.0), 1)
        description = fake.text(max_nb_chars=2000)
        smi_date = fake.date_this_decade()

        cursor.execute("""
            INSERT INTO short_medical_interviews (symptoms, temperature, description, smi_date, user_id)
            VALUES (%s, %s, %s, %s, %s);
        """, (symptoms, temperature, description, smi_date, user_id))

def generate_and_insert_data_postgres():
    """Główna funkcja do generowania danych i ich wstawiania do bazy."""
    fake = Faker()

    # Czyszczenie bazy przed dodaniem nowych danych
    clear_database()

    conn = psycopg2.connect(#database="postgres", user="postgres", password="admin"
        #**DB_CONFIG
        host="localhost",
        port=5433,
        database="healthcare-postgres",
        user="healthcare",
        password="root"
    )
    cursor = conn.cursor()

    users = generate_users(cursor, fake, DATA_CONFIG["num_users"])
    doctors = generate_doctors(cursor, fake, DATA_CONFIG["num_doctors"])
    clinics = generate_clinics(cursor, fake, DATA_CONFIG["num_clinics"])
    generate_examinations(cursor, fake, users, doctors, DATA_CONFIG["num_examinations"])
    generate_user_basic_data(cursor, fake, users, DATA_CONFIG["num_user_basic_data"])
    generate_medical_interviews(cursor, fake, users, DATA_CONFIG["num_medical_interviews"])

    conn.commit()
    cursor.close()
    conn.close()
    print("Data has been successfully added to PostgresSQL!")
