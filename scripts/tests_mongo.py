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

def crud_mongo():
    try:
        # Połączenie z MongoDB
        client = pymongo.MongoClient(**DB_CONFIG["mongo"])
        db = client["healthcare_mongo"]
        collection = db["healthcare_collection"]

        # CREATE
        start_time = time.time()
        collection.insert_one({"column1": "test1", "column2": "value1"})
        print("MongoDB CREATE Time:", time.time() - start_time)

        # READ
        start_time = time.time()
        collection.find_one({"column1": "test1"})
        print("MongoDB READ Time:", time.time() - start_time)

        # UPDATE
        start_time = time.time()
        collection.update_one({"column1": "test1"}, {"$set": {"column1": "updated_value"}})
        print("MongoDB UPDATE Time:", time.time() - start_time)

        # DELETE
        start_time = time.time()
        collection.delete_one({"column1": "updated_value"})
        print("MongoDB DELETE Time:", time.time() - start_time)

    except Exception as e:
        print("MongoDB CRUD Test failed:", e)
