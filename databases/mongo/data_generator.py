import pymongo
from faker import Faker
import random

DB_CONFIG = {
    "host": "localhost",
    "port": 27017,
    "username": "root",
    "password": "example"
}

DATA_CONFIG = {
    "num_users": 100,
    "num_doctors": 10,
    "num_clinics": 10,
    "num_examinations": 200,
    "num_user_basic_data": 100,  # Liczba użytkowników z podstawowymi danymi
    "num_medical_interviews": 100  # Liczba użytkowników z wywiadami medycznymi
}

client = pymongo.MongoClient(f"mongodb://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/")
db = client["healthcare-mongo"]

fake = Faker()

def clear_database():
    db.users.drop()
    db.doctors.drop()
    db.clinics.drop()
    db.examinations.drop()
    db.user_basic_data.drop()
    db.short_medical_interviews.drop()
    db.doctor_clinic.drop()
    print("\nThe MongoDB database has been successfully cleared!")

def generate_users(num_users):
    return [{
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": fake.phone_number()[:14],
        "email": fake.unique.email(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        "gender": random.choice(["male", "female"]),
        "pesel": str(fake.random_int(min=10000000000, max=99999999999))
    } for _ in range(num_users)]

def generate_doctors(num_doctors):
    return [{
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": fake.phone_number()[:14],
        "email": fake.unique.email(),
        "gender": random.choice(["male", "female"])
    } for _ in range(num_doctors)]

def generate_clinics(num_clinics):
    return [{
        "name": fake.company(),
        "address": fake.address(),
        "phone": fake.phone_number()[:14]
    } for _ in range(num_clinics)]

def generate_examinations(users, doctors, num_examinations):
    return [{
        "name": fake.word(),
        "examination_date": fake.date_this_year().isoformat(),
        "doctor_id": random.choice(doctors)["_id"],
        "user_id": random.choice(users)["_id"]
    } for _ in range(num_examinations)]

def generate_user_basic_data(users, num_entries):
    selected_users = random.sample(users, min(num_entries, len(users)))
    return [{
        "user_id": user["_id"],
        "weight": round(random.uniform(50, 120), 2),
        "height": random.randint(150, 200),
        "systolic_pressure": random.randint(90, 140),
        "diastolic_pressure": random.randint(60, 90),
        "temperature": round(random.uniform(36.0, 39.0), 1),
        "entry_date": fake.date_this_decade().isoformat()
    } for user in selected_users]

def generate_medical_interviews(users, num_entries):
    selected_users = random.sample(users, min(num_entries, len(users)))
    symptoms_list = ["pain", "sticky", "press", "other"]
    return [{
        "user_id": user["_id"],
        "symptoms": random.choice(symptoms_list),
        "temperature": round(random.uniform(36.0, 39.0), 1),
        "description": fake.text(max_nb_chars=2000),
        "smi_date": fake.date_this_decade().isoformat()
    } for user in selected_users]

def generate_doctor_clinic_relationships(doctors, clinics):
    return [{
        "doctor_id": doctor["_id"],
        "clinic_id": random.choice(clinics)["_id"]
    } for doctor in doctors]

def generate_and_insert_data_mongo():
    clear_database()

    users = generate_users(DATA_CONFIG["num_users"])
    db.users.insert_many(users)
    users = list(db.users.find())

    doctors = generate_doctors(DATA_CONFIG["num_doctors"])
    db.doctors.insert_many(doctors)
    doctors = list(db.doctors.find())

    clinics = generate_clinics(DATA_CONFIG["num_clinics"])
    db.clinics.insert_many(clinics)
    clinics = list(db.clinics.find())

    examinations = generate_examinations(users, doctors, DATA_CONFIG["num_examinations"])
    db.examinations.insert_many(examinations)

    user_basic_data = generate_user_basic_data(users, DATA_CONFIG["num_user_basic_data"])
    if user_basic_data:
        db.user_basic_data.insert_many(user_basic_data)

    medical_interviews = generate_medical_interviews(users, DATA_CONFIG["num_medical_interviews"])
    if medical_interviews:
        db.short_medical_interviews.insert_many(medical_interviews)

    doctor_clinic_relationships = generate_doctor_clinic_relationships(doctors, clinics)
    db.doctor_clinic.insert_many(doctor_clinic_relationships)

    print("Data has been successfully added to MongoDB!")