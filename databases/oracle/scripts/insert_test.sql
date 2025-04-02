DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    start_time := SYSTIMESTAMP;

    FOR i IN 1..1000000 LOOP
        INSERT INTO users (user_id, first_name, last_name, phone, email, pesel, gender)
        VALUES (users_seq.NEXTVAL, 'Test', 'User', '123456789', 'test'||i||'@example.com', '12345678901', 'male');
    END LOOP;

    COMMIT;

    end_time := SYSTIMESTAMP;
    DBMS_OUTPUT.put_line('INSERT Execution time: ' || (end_time - start_time));
END;
/