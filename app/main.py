import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION")
JSONL_FILE = os.getenv("JSONL_FILE")

client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

with open(JSONL_FILE, "r", encoding="utf-8") as f:
    documents = [json.loads(line) for line in f if line.strip()]

if documents:
    result = collection.insert_many(documents)
    print(f"{len(result.inserted_ids)} documents inserted successfully!")
else:
    print("No documents found in the JSONL.")
