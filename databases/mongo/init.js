db = db.getSiblingDB("healthcare-mongo");

db.createUser({
    user: "root",
    pwd: "example",
    roles: [
        { role: "readWrite", db: "healthcare-mongo" }
    ]
});

db.createCollection("users");
db.createCollection("doctors");
db.createCollection("clinics");
db.createCollection("examinations");
db.createCollection("user_basic_data");
db.createCollection("short_medical_interviews");
db.createCollection("doctor_clinic");

print("MongoDB initialization completed.");
