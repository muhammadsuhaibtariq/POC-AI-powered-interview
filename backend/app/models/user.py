from pydantic import BaseModel, EmailStr
from typing import List

class User(BaseModel):
    email: EmailStr
    name: str


class SaveResponseRequest(BaseModel):
    email: EmailStr
    persona: str
    answers: List[str]  # Expecting a **list of answers**