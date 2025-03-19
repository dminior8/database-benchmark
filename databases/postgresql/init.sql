-- Tworzenie typu ENUM dla plci
CREATE TYPE gender_enum AS ENUM ('male', 'female');
CREATE TYPE symptoms_enum AS ENUM ('pain', 'sticky', 'press', 'other');

-- Tabela uzytkownikow
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(14) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    birth_date DATE,
    gender gender_enum,
    pesel VARCHAR(11) NOT NULL
);

-- Tabela lekarzy
CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(14) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    gender gender_enum
);

-- Tabela przychodni
CREATE TABLE clinics (
    clinic_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(14) UNIQUE NOT NULL
);

-- Tabela badań
CREATE TABLE examinations (
    examination_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    examination_date DATE,
    doctor_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabela danych podstawowych użytkownika
CREATE TABLE users_basic_data (
    user_id INT PRIMARY KEY NOT NULL,
    weight DOUBLE PRECISION,
    height INT,
    systolic_pressure INT,
    diastolic_pressure INT,
    temperature DOUBLE PRECISION,
    entry_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabela krótkich wywiadów medycznych
CREATE TABLE short_medical_interviews (
    registration_nr SERIAL PRIMARY KEY,
    symptoms symptoms_enum NOT NULL,
    temperature DOUBLE PRECISION NOT NULL,
    description VARCHAR(2000),
    smi_date DATE NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabela powiązań lekarzy z przychodniami
CREATE TABLE doctors_clinics (
    doctor_id INT NOT NULL,
    clinic_id INT NOT NULL,
    PRIMARY KEY (doctor_id, clinic_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (clinic_id) REFERENCES clinics(clinic_id)
);