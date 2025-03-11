from ..config.vector_db import index_1 as index
from ..utils.embeddings import get_embedding

def fetch_hr_questions(job_description: str, top_k: int = 10):
    # Convert the job description into an embedding
    query_embedding = get_embedding(job_description)

    # Query Pinecone for similar HR questions
    query_response = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    questions = []
    for match in query_response.get("matches", []):
        metadata = match.get("metadata", {})
        question = metadata.get("question")
        if question:
            questions.append(question)

    return {"questions": questions}