from pymongo import MongoClient
from settings import MONGO_USER, MONGO_PASS, MONGO_HOST, DATABASE_NAME, COLLECTION_NAME
from urllib.parse import quote_plus

uri = "mongodb://%s:%s@%s" % (
    quote_plus(MONGO_USER), quote_plus(MONGO_PASS), MONGO_HOST)
client = MongoClient(uri)
db = client[DATABASE_NAME] 

def insert(doc):
    db[COLLECTION_NAME].insert_one(doc)