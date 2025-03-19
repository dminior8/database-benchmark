import oracledb
from faker import Faker
import random
import uuid  # Importujemy bibliotekę do generowania UUID

# Konfiguracja bazy danych
DB_CONFIG = {
    "dsn": "localhost:1521/XE",  # Upewnij się, że to jest poprawny DSN
    "user": "SYS",
    "password": "YourPassword123",
    "mode": oracledb.SYSDBA  # Tutaj ustawiamy tryb SYSDBA
}

DATA_CONFIG = {
    "num_users": 100,
    "num_doctors": 10,
    "num_clinics": 10,
    "num_examinations": 200,
    "num_user_basic_data": 100,
    "num_medical_interviews": 100
}


def get_connection():
    return oracledb.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            dsn=DB_CONFIG["dsn"],
            mode=oracledb.SYSDBA
        )


def clear_database():
    """Usuwa dane z tabel przed dodaniem nowych."""
    conn = get_connection()
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
        try:
            cursor.execute(f"DELETE FROM {table}")
        except oracledb.DatabaseError:
            pass  # Ignorujemy błąd, jeśli tabela nie istnieje

    conn.commit()
    cursor.close()
    conn.close()
    print("\nThe Oracle database has been successfully cleared!")


def generate_users(cursor, fake, num_users):
    """Generuje użytkowników i zwraca ich ID."""
    user_ids = []

    for _ in range(num_users):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.phone_number()[:14]
        email = fake.unique.email()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
        gender = fake.random_element(elements=('male', 'female'))
        pesel = str(fake.random_int(min=10000000000, max=99999999999))

        # Tworzymy zmienną do przechowywania zwróconego user_id
        user_id_var = cursor.var(int)

        # Wstawiamy dane, a Oracle zwróci wygenerowany user_id
        cursor.execute("""
            INSERT INTO users (user_id, first_name, last_name, phone, email, birth_date, gender, pesel)
            VALUES (users_seq.NEXTVAL, :1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6, :7)
            RETURNING user_id INTO :8
        """, (first_name, last_name, phone, email, birth_date, gender, pesel, user_id_var))

        # Pobieramy wartość user_id zwróconą przez Oracle
        user_id = user_id_var.getvalue()[0]
        user_ids.append(user_id)  # Dodajemy do listy

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

        doctor_id_var = cursor.var(int)

        cursor.execute("""
            INSERT INTO doctors (doctor_id, first_name, last_name, phone, email, gender)
            VALUES (doctors_seq.NEXTVAL, :1, :2, :3, :4, :5)
            RETURNING doctor_id INTO :6
        """, (first_name, last_name, phone, email, gender, doctor_id_var))

        doctor_id = doctor_id_var.getvalue()[0]
        doctor_ids.append(doctor_id)

    return doctor_ids


def generate_clinics(cursor, fake, num_clinics):
    """Generuje przychodnie i zwraca ich ID."""
    clinic_ids = []

    for _ in range(num_clinics):
        name = fake.company()
        address = fake.address()
        phone = fake.phone_number()[:14]

        clinic_id_var = cursor.var(int)

        cursor.execute("""
            INSERT INTO clinics (clinic_id, name, address, phone)
            VALUES (clinics_seq.NEXTVAL, :1, :2, :3)
            RETURNING clinic_id INTO :4
        """, (name, address, phone, clinic_id_var))

        clinic_id = clinic_id_var.getvalue()[0]
        clinic_ids.append(clinic_id)

    return clinic_ids


def generate_examinations(cursor, fake, users, doctors, num_examinations):
    """Generuje badania medyczne."""
    for _ in range(num_examinations):
        name = fake.word()
        exam_date = fake.date_this_decade().strftime('%Y-%m-%d')
        doctor_id = random.choice(doctors)
        user_id = random.choice(users)

        cursor.execute("""
            INSERT INTO examinations (examination_id, name, examination_date, doctor_id, user_id)
            VALUES (examinations_seq.NEXTVAL, :1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4)
        """, (name, exam_date, doctor_id, user_id))


def generate_user_basic_data(cursor, fake, users, num_entries):
    """Generuje podstawowe dane dla określonej liczby użytkowników."""
    selected_users = random.sample(users, min(num_entries, len(users)))

    for user_id in selected_users:
        weight = round(random.uniform(50, 120), 2)
        height = random.randint(150, 200)
        systolic_pressure = random.randint(90, 140)
        diastolic_pressure = random.randint(60, 90)
        temperature = round(random.uniform(36.0, 39.0), 1)
        entry_date = fake.date_this_decade().strftime('%Y-%m-%d')

        cursor.execute("""
            INSERT INTO users_basic_data (user_id, weight, height, systolic_pressure, diastolic_pressure, temperature, entry_date)
            VALUES (:1, :2, :3, :4, :5, :6, TO_DATE(:7, 'YYYY-MM-DD'))
        """, (user_id, weight, height, systolic_pressure, diastolic_pressure, temperature, entry_date))


def generate_medical_interviews(cursor, fake, users, num_entries):
    """Generuje wywiady medyczne dla określonej liczby użytkowników."""
    selected_users = random.sample(users, min(num_entries, len(users)))

    for user_id in selected_users:
        symptoms = fake.random_element(elements=('pain', 'sticky', 'press', 'other'))
        temperature = round(random.uniform(36.0, 39.0), 1)
        description = fake.text(max_nb_chars=2000)
        smi_date = fake.date_this_decade().strftime('%Y-%m-%d')

        cursor.execute("""
            INSERT INTO short_medical_interviews (registration_nr, symptoms, temperature, description, smi_date, user_id)
            VALUES (short_medical_interviews_seq.NEXTVAL, :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5)
        """, (symptoms, temperature, description, smi_date, user_id))

def generate_and_insert_data_oracle():
    """Główna funkcja do generowania danych i ich wstawiania do bazy Oracle."""
    fake = Faker()

    clear_database()

    conn = get_connection()
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
    print("Data has been successfully added to Oracle!")
