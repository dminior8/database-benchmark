-- Zaloguj się jako SYSDBA
CONNECT SYS/YourSysPassword AS SYSDBA;

-- Udziel uprawnień użytkownikowi C##healthcare
GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO C##healthcare;
GRANT CREATE TRIGGER TO C##healthcare;


-- Tworzymy użytkownika i schemat healthcare
CREATE USER C##healthcare IDENTIFIED BY "YourPassword123";

-- Przydzielamy odpowiednie uprawnienia
GRANT CONNECT, RESOURCE, DBA TO C##healthcare;

-- Ustawiamy healthcare jako właściciela tabel
ALTER USER C##healthcare QUOTA UNLIMITED ON USERS;

-- Tworzenie ENUM jako tabeli w Oracle
CREATE TABLE gender_enum (value VARCHAR2(10) PRIMARY KEY);
INSERT INTO gender_enum (value) VALUES ('male');
INSERT INTO gender_enum (value) VALUES ('female');

CREATE TABLE symptoms_enum (value VARCHAR2(10) PRIMARY KEY);
INSERT INTO symptoms_enum (value) VALUES ('pain');
INSERT INTO symptoms_enum (value) VALUES ('sticky');
INSERT INTO symptoms_enum (value) VALUES ('press');
INSERT INTO symptoms_enum (value) VALUES ('other');

-- Sekwencje dla tabel
CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE doctors_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE clinics_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE examinations_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE smi_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE short_medical_interviews_seq START WITH 1 INCREMENT BY 1;


-- Tabela użytkowników
CREATE TABLE users (
    user_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(255) NOT NULL,
    last_name VARCHAR2(255) NOT NULL,
    phone VARCHAR2(14) NOT NULL,
    email VARCHAR2(255) UNIQUE NOT NULL,
    birth_date DATE,
    gender VARCHAR2(10) CHECK (gender IN ('male', 'female')),
    pesel VARCHAR2(11) NOT NULL
);

-- Tabela lekarzy
CREATE TABLE doctors (
    doctor_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(255) NOT NULL,
    last_name VARCHAR2(255) NOT NULL,
    phone VARCHAR2(14) NOT NULL,
    email VARCHAR2(255) UNIQUE NOT NULL,
    gender VARCHAR2(10) CHECK (gender IN ('male', 'female'))
);

-- Tabela przychodni
CREATE TABLE clinics (
    clinic_id NUMBER PRIMARY KEY,
    name VARCHAR2(255) NOT NULL,
    address VARCHAR2(255) NOT NULL,
    phone VARCHAR2(14) UNIQUE NOT NULL
);

-- Tabela badań
CREATE TABLE examinations (
    examination_id NUMBER PRIMARY KEY,
    name VARCHAR2(200) NOT NULL,
    examination_date DATE,
    doctor_id NUMBER NOT NULL,
    user_id NUMBER NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabela danych podstawowych użytkownika
CREATE TABLE users_basic_data (
    user_id NUMBER PRIMARY KEY NOT NULL,
    weight NUMBER(5,2),
    height NUMBER(3),
    systolic_pressure NUMBER(3),
    diastolic_pressure NUMBER(3),
    temperature NUMBER(3,1),
    entry_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabela krótkich wywiadów medycznych
CREATE TABLE short_medical_interviews (
    registration_nr NUMBER PRIMARY KEY,
    symptoms VARCHAR2(10) CHECK (symptoms IN ('pain', 'sticky', 'press', 'other')),
    temperature NUMBER(3,1) NOT NULL,
    description VARCHAR2(2000),
    smi_date DATE NOT NULL,
    user_id NUMBER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tabela powiązań lekarzy z przychodniami
CREATE TABLE doctors_clinics (
    doctor_id NUMBER NOT NULL,
    clinic_id NUMBER NOT NULL,
    PRIMARY KEY (doctor_id, clinic_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (clinic_id) REFERENCES clinics(clinic_id)
);

-- Triggery do automatycznego przypisywania ID
CREATE OR REPLACE TRIGGER users_trigger
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    SELECT users_seq.NEXTVAL INTO :NEW.user_id FROM dual;
END;

CREATE OR REPLACE TRIGGER doctors_trigger
BEFORE INSERT ON doctors
FOR EACH ROW
BEGIN
    SELECT doctors_seq.NEXTVAL INTO :NEW.doctor_id FROM dual;
END;

CREATE OR REPLACE TRIGGER clinics_trigger
BEFORE INSERT ON clinics
FOR EACH ROW
BEGIN
    SELECT clinics_seq.NEXTVAL INTO :NEW.clinic_id FROM dual;
END;

CREATE OR REPLACE TRIGGER examinations_trigger
BEFORE INSERT ON examinations
FOR EACH ROW
BEGIN
    SELECT examinations_seq.NEXTVAL INTO :NEW.examination_id FROM dual;
END;

CREATE OR REPLACE TRIGGER smi_trigger
BEFORE INSERT ON short_medical_interviews
FOR EACH ROW
BEGIN
    SELECT smi_seq.NEXTVAL INTO :NEW.registration_nr FROM dual;
END;

DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    start_time := SYSTIMESTAMP;

    FOR rec IN (SELECT * FROM users WHERE rownum <= 1000000) LOOP
        NULL;
    END LOOP;

    end_time := SYSTIMESTAMP;
    DBMS_OUTPUT.put_line('SELECT Execution time: ' || (end_time - start_time));
END;
/
