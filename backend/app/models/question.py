from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    email: str
    job_description: str
    persona: str

class QuestionResponse(BaseModel):
    questions: List[str]
    suggested_answers: List[str]

class HRQuestionRequest(BaseModel):
    job_description: str
    top_k: int = 10