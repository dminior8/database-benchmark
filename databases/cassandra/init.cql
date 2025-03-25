-- Tworzenie keyspace
CREATE KEYSPACE healthcare
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE healthcare;

-- Tabela użytkowników
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT,
    birth_date DATE,
    gender TEXT,
    pesel TEXT
);

-- Tabela lekarzy
CREATE TABLE doctors (
    doctor_id UUID PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT,
    gender TEXT
);

-- Tabela przychodni
CREATE TABLE clinics (
    clinic_id UUID PRIMARY KEY,
    name TEXT,
    address TEXT,
    phone TEXT
);

-- Tabela badań
CREATE TABLE examinations (
    examination_id UUID PRIMARY KEY,
    name TEXT,
    examination_date DATE,
    doctor_id UUID,
    user_id UUID
);

-- Tabela danych podstawowych użytkownika
CREATE TABLE users_basic_data (
    user_id UUID PRIMARY KEY,
    weight DOUBLE,
    height INT,
    systolic_pressure INT,
    diastolic_pressure INT,
    temperature DOUBLE,
    entry_date DATE
);

-- Tabela krótkich wywiadów medycznych
CREATE TABLE short_medical_interviews (
    registration_nr UUID PRIMARY KEY,
    symptoms TEXT,
    temperature DOUBLE,
    description TEXT,
    smi_date DATE,
    user_id UUID
);

-- Tabela powiązań lekarzy z przychodniami (denormalizacja: nie ma JOIN-ów w Cassandrze)
CREATE TABLE doctors_clinics (
    doctor_id UUID,
    clinic_id UUID,
    PRIMARY KEY (doctor_id, clinic_id)
);