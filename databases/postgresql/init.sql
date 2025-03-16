CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    age INT
);

INSERT INTO users (name, email, age) VALUES
    ('Alice Johnson', 'alice@example.com', 28),
    ('Bob Smith', 'bob@example.com', 35),
    ('Charlie Brown', 'charlie@example.com', 40);
