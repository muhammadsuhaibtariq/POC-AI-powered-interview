from pymongo import MongoClient
import os
from dotenv import load_dotenv


# Load environment variables from a .env file
load_dotenv()

# Get the MongoDB URI from the environment variables (set in Vercel)
MONGODB_URI_FASTAPI = os.getenv("MONGODB_URI_FASTAPI")

# Create a new MongoDB client and connect to the server using the URI
mongo_client = MongoClient(MONGODB_URI_FASTAPI)

db = mongo_client["ai_powered_interview_question_db"]
users_collection = db["users"]
