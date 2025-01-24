from pymongo import MongoClient
import os


_db = None


def connect_to_mongo():
    global _db
    if _db is None:
        mongo_uri = os.getenv("MONGO_URI")
        client = MongoClient(mongo_uri)
        _db = client["forecast"]
        print(
            f"_db: {_db}",
        )
    return _db


def get_db_instance():
    """Return the database instance, ensuring it's initialized."""
    if _db is None:
        return connect_to_mongo()
    return _db
