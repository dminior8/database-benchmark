CREATE KEYSPACE IF NOT EXISTS test_keyspace
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE test_keyspace;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INT
);

INSERT INTO users (id, name, email, age) VALUES
    (uuid(), 'Alice Johnson', 'alice@example.com', 28);
INSERT INTO users (id, name, email, age) VALUES
    (uuid(), 'Bob Smith', 'bob@example.com', 35);
INSERT INTO users (id, name, email, age) VALUES
    (uuid(), 'Charlie Brown', 'charlie@example.com', 40);
