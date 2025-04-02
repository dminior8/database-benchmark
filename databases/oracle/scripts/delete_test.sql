DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    start_time := SYSTIMESTAMP;

    FOR i IN 1..1000000 LOOP
        DELETE FROM users WHERE user_id = i;
    END LOOP;

    COMMIT;

    end_time := SYSTIMESTAMP;
    DBMS_OUTPUT.put_line('DELETE Execution time: ' || (end_time - start_time));
END;
/
