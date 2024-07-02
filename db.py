from pymongo import MongoClient

client = None
db = None
collection = None

def initialize_db():
    global client, db, collection
    client = MongoClient("mongodb://localhost:27017/")
    db = client.mqtt_db
    collection = db.messages
    print("MongoDB connection established.")

def close_db_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")
        
def get_collection():
    return collection

