import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URL")

if not MONGO_URL:
    raise ValueError("MONGODB_URL is not set in .env file")

client = MongoClient(MONGO_URL)

db = client["ai_interview_assistant"]
chat_collection = db["chats"]