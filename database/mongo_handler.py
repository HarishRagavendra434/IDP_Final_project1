
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

database = client["idp_database"]

collection = database["documents"]

def store_results(filename, document_type, results):

    document = {
        "filename": filename,
        "document_type": document_type,
        "results": results
    }

    collection.insert_one(document)
