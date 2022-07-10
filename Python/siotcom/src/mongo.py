#!/usr/bin/env python

# 2022 SYST, Universidad Politecnica de Madrid
# SIoTCom
# @File : mongo.py
# @Author : a.cvillasenor@alumnos.upm.es
# This takes data from source and connects to MongoDB

# Local imports

# External imports
import pymongo
import json
from pymongo.errors import ConnectionFailure

#Global Config
MONGO_URI = "mongodb://127.0.0.1:27017/"  # mongodb://ip:port if connecting remotely
MONGO_DB = "siotcom"
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
        print("Connecting to MongoDB")

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
        print("Disconnected from MongoDB")
    
    def save(self, msg):
        if self.on_Connect():
            try:
                result = self.collection.insert_one(json.loads(msg))
                print("Saved document with id ", result.inserted_id)
            except Exception as ex:
                print(ex)
        else:
            print("Could not store data in MongoDB")
