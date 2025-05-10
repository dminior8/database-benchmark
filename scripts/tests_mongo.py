import uuid
from datetime import datetime

import pymongo
import time

DB_CONFIG = {
    "mongo": {
        "host": "localhost",
        "port": 27017,
        "username": "root",
        "password": "example"
    }
}

TEST_CASES = [100, 200, 300, 500, 1_000, 5_000, 10_000, 15_000, 20_000]


def crud_mongo():
    create_times = []
    read_times = []
    update_times = []
    delete_times = []

    client = pymongo.MongoClient(**DB_CONFIG["mongo"])
    db = client["healthcare_mongo"]
    coll = db["healthcare_collection"]

    for n in TEST_CASES:
        # CREATE
        start = time.time()
        for _ in range(n):
            coll.insert_one({
                "user_id": str(uuid.uuid4()),
                "first_name": "John",
                "last_name": "Doe",
                "phone": "123456789",
                "email": "john.doe@example.com",
                "birth_date": datetime.strptime("1990-01-01", "%Y-%m-%d"),
                "gender": "male",
                "pesel": "12345678901"
            })
        create_times.append(time.time() - start)

        # READ
        start = time.time()
        for _ in range(n):
            coll.find_one({"first_name": "John", "last_name": "Doe"})
        read_times.append(time.time() - start)

        # UPDATE
        start = time.time()
        for _ in range(n):
            coll.update_one(
                {"first_name": "John", "last_name": "Doe"},
                {"$set": {"first_name": "Jane"}}
            )
        update_times.append(time.time() - start)

        # DELETE
        start = time.time()
        for _ in range(n):
            coll.delete_one({"first_name": "Jane", "last_name": "Doe"})
        delete_times.append(time.time() - start)

    client.close()

    return [
        TEST_CASES,
        create_times,
        read_times,
        update_times,
        delete_times,
        "MongoDB",
        "orange"
    ]
