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
