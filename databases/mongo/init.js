db = db.getSiblingDB('testdb');

db.users.insertMany([
    { name: "Alice Johnson", email: "alice@example.com", age: 28 },
    { name: "Bob Smith", email: "bob@example.com", age: 35 },
    { name: "Charlie Brown", email: "charlie@example.com", age: 40 }
]);

print("MongoDB initialization completed.");
