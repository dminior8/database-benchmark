CREATE TABLE users (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100),
    email VARCHAR2(100) UNIQUE,
    age NUMBER
);

INSERT INTO users (name, email, age) VALUES
    ('Alice Johnson', 'alice@example.com', 28);
INSERT INTO users (name, email, age) VALUES
    ('Bob Smith', 'bob@example.com', 35);
INSERT INTO users (name, email, age) VALUES
    ('Charlie Brown', 'charlie@example.com', 40);

COMMIT;
