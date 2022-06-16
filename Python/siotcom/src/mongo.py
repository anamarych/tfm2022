#Local imports

#External imports
import pymongo
import json
from pymongo.errors import ConnectionFailure

#Global Config
MONGO_URI = "mongodb://127.0.0.1:27017/"  # mongodb://ip:port
MONGO_DB = "SIoTCom"
MONGO_COLLECTION = "sensor"

class Mongo():
    def __init__(self):
        self.client: pymongo.MongoClient = None
        self.database: pymongo.database.Database = None
        self.collection: pymongo.collection.Collection = None
        
    def connect(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.database = self.client[MONGO_DB]
        self.collection = self.database[MONGO_COLLECTION]
        print("Connecting")

    def on_Connect(self):
        if self.client:
            try:
                # The ismaster command does not require auth
                self.client.admin.command("ismaster")
                return True
            except ConnectionFailure:
                return False
        else:
            return False

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
        print("Disconnected")
    
    def save(self, msg):
        print("Storing data")
        if self.on_Connect():
            try:
                result = self.collection.insert_one(json.loads(msg))
                print("Saved document with id ", result.inserted_id)
            except Exception as ex:
                print(ex)
        else:
            print("Could not store data")
