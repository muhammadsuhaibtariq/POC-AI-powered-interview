from pinecone import Pinecone, ServerlessSpec
import time

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(PINECONE_API_KEY)
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

index_1 = "hr-questions"

if index_1 not in existing_indexes:
    pc.create_index(
        name=index_1,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_1).status["ready"]:
        time.sleep(1)


# Get the index
index_1 = pc.Index(index_1)
