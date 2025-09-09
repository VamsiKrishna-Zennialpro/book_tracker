#passkey: oaJbD6sowGS6bZes@resumestore.egj3wqb
#mongo_cluster = "mongodb+srv://vamsikrishnapanga77:oaJbD6sowGS6bZes@resumestore.egj3wqb.mongodb.net/"

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
#from pymongo import MongoClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://vamsikrishnapanga77:oaJbD6sowGS6bZes@resumestore.egj3wqb.mongodb.net/")

database_name = "book_tracker"
collection_one = "books"
collection_two = "users"

#client = MongoClient(MONGO_URL)
client = AsyncIOMotorClient(MONGO_URL)
db = client[database_name]
books_collection = db[collection_one]
users_collection = db[collection_two]

books_db={}