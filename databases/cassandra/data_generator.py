from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from faker import Faker
import random
import uuid

# Konfiguracja bazy Cassandra
CASSANDRA_CONFIG = {
    "host": "localhost",
    "port": 9042,
    "keyspace": "healthcare"
}

DATA_CONFIG = {
    "num_users": 100,
    "num_doctors": 10,
    "num_clinics": 10,
    "num_examinations": 200,
    "num_user_basic_data": 100,
    "num_medical_interviews": 100
}


def connect_to_cassandra():
    """Nawiązuje połączenie z Cassandra DB."""
    cluster = Cluster([CASSANDRA_CONFIG["host"]], port=CASSANDRA_CONFIG["port"])
    session = cluster.connect()
    session.set_keyspace(CASSANDRA_CONFIG["keyspace"])
    return session


def clear_database(session):
    """Usuwa wszystkie dane z tabel."""
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
        session.execute(f"TRUNCATE {table};")
    print("\nThe Cassandra database has been successfully cleared!")


def generate_users(session, fake, num_users):
    """Generuje użytkowników."""
    user_ids = []
    for _ in range(num_users):
        user_id = uuid.uuid4()
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.phone_number()[:14]
        email = fake.unique.email()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
        gender = fake.random_element(elements=('male', 'female'))
        pesel = str(fake.random_int(min=10000000000, max=99999999999))

        session.execute("""
            INSERT INTO users (user_id, first_name, last_name, phone, email, birth_date, gender, pesel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (user_id, first_name, last_name, phone, email, birth_date, gender, pesel))
        user_ids.append(user_id)

    return user_ids


def generate_doctors(session, fake, num_doctors):
    """Generuje lekarzy."""
    doctor_ids = []
    for _ in range(num_doctors):
        doctor_id = uuid.uuid4()
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.phone_number()[:14]
        email = fake.unique.email()
        gender = fake.random_element(elements=('male', 'female'))

        session.execute("""
            INSERT INTO doctors (doctor_id, first_name, last_name, phone, email, gender)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (doctor_id, first_name, last_name, phone, email, gender))
        doctor_ids.append(doctor_id)

    return doctor_ids


def generate_clinics(session, fake, num_clinics):
    """Generuje przychodnie."""
    clinic_ids = []
    for _ in range(num_clinics):
        clinic_id = uuid.uuid4()
        name = fake.company()
        address = fake.address()
        phone = fake.phone_number()[:14]

        session.execute("""
            INSERT INTO clinics (clinic_id, name, address, phone)
            VALUES (%s, %s, %s, %s);
        """, (clinic_id, name, address, phone))
        clinic_ids.append(clinic_id)

    return clinic_ids


def generate_examinations(session, fake, users, doctors, num_examinations):
    """Generuje badania."""
    for _ in range(num_examinations):
        examination_id = uuid.uuid4()
        name = fake.word()
        exam_date = fake.date_this_decade()
        doctor_id = random.choice(doctors)
        user_id = random.choice(users)

        session.execute("""
            INSERT INTO examinations (examination_id, name, examination_date, doctor_id, user_id)
            VALUES (%s, %s, %s, %s, %s);
        """, (examination_id, name, exam_date, doctor_id, user_id))


def generate_user_basic_data(session, fake, users, num_entries):
    """Generuje podstawowe dane użytkowników."""
    selected_users = random.sample(users, min(num_entries, len(users)))

    for user_id in selected_users:
        weight = round(random.uniform(50, 120), 2)
        height = random.randint(150, 200)
        systolic_pressure = random.randint(90, 140)
        diastolic_pressure = random.randint(60, 90)
        temperature = round(random.uniform(36.0, 39.0), 1)
        entry_date = fake.date_this_decade()

        session.execute("""
            INSERT INTO users_basic_data (user_id, weight, height, systolic_pressure, diastolic_pressure, temperature, entry_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (user_id, weight, height, systolic_pressure, diastolic_pressure, temperature, entry_date))


def generate_medical_interviews(session, fake, users, num_entries):
    """Generuje krótkie wywiady medyczne."""
    selected_users = random.sample(users, min(num_entries, len(users)))

    for user_id in selected_users:
        registration_nr = uuid.uuid4()
        symptoms = fake.random_element(elements=('pain', 'sticky', 'press', 'other'))
        temperature = round(random.uniform(36.0, 39.0), 1)
        description = fake.text(max_nb_chars=2000)
        smi_date = fake.date_this_decade()

        session.execute("""
            INSERT INTO short_medical_interviews (registration_nr, symptoms, temperature, description, smi_date, user_id)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (registration_nr, symptoms, temperature, description, smi_date, user_id))


def generate_doctors_clinics(session, doctors, clinics):
    """Generuje powiązania lekarzy z przychodniami."""
    for doctor_id in doctors:
        assigned_clinics = random.sample(clinics, random.randint(1, len(clinics) // 2))
        for clinic_id in assigned_clinics:
            session.execute("""
                INSERT INTO doctors_clinics (doctor_id, clinic_id)
                VALUES (%s, %s);
            """, (doctor_id, clinic_id))


def generate_and_insert_data_cassandra():
    """Główna funkcja do generowania danych i ich wstawiania do Cassandry."""
    session = connect_to_cassandra()
    fake = Faker()

    # Czyszczenie bazy
    clear_database(session)

    # Generowanie danych
    users = generate_users(session, fake, DATA_CONFIG["num_users"])
    doctors = generate_doctors(session, fake, DATA_CONFIG["num_doctors"])
    clinics = generate_clinics(session, fake, DATA_CONFIG["num_clinics"])
    generate_examinations(session, fake, users, doctors, DATA_CONFIG["num_examinations"])
    generate_user_basic_data(session, fake, users, DATA_CONFIG["num_user_basic_data"])
    generate_medical_interviews(session, fake, users, DATA_CONFIG["num_medical_interviews"])
    generate_doctors_clinics(session, doctors, clinics)

    print("Data has been successfully added to Cassandra!")
