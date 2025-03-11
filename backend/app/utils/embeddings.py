from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import os
from typing import List
from dotenv import load_dotenv
load_dotenv()

# Retrieve the OpenAI API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key)
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
)

def get_embedding(texts: str) -> List[float]:
    try:
        # Replace newlines in text with spaces, as per API documentation
        texts = texts.replace("\n", " ")
        single_vector = embeddings.embed_query(texts)

    except Exception as e:
        print(f"Error while generating embeddings: {e}")
        return []

    return single_vector
