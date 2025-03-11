from dotenv import load_dotenv
import os

from openai import OpenAI
from ..models.question import QuestionResponse
from ..utils.load_prompts import load_prompt
from ..services.fetch_questions import fetch_hr_questions

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Persona-to-role mapping
persona_roles = {
    "HR": "HR specialist",
    "Recruiter": "recruiter",
    "Hiring Manager": "hiring manager",
    "Technical Interviewer": "technical expert"
}

def generate_interview_questions(persona: str, job_description: str):
    try:
        # Prepare the system message to guide the AI
        system_message = load_prompt("system", "interview_questions.txt")  # Load system prompt

        # Map persona to corresponding prompt file
        persona_prompts = {
            "HR": "hr.txt",
            "Recruiter": "recruiter.txt",
            "Hiring Manager": "hiring_manager.txt",
            "Technical Interviewer": "technical_interviewer.txt",
        }

        hr_questions = fetch_hr_questions(job_description, top_k=15)
        prompt_file = persona_prompts.get(persona, "general.txt")  # Default to general.txt
        user_prompt = load_prompt("user", prompt_file).format(
            hr_questions=hr_questions,
            job_description=job_description)

        print(f"User prompt: {user_prompt}")

        # API call to OpenAI GPT model
        completion = client.beta.chat.completions.parse(  # Ensure structured response
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt},
            ],
            response_format=QuestionResponse
        )

        # Debugging: Check the raw response
        raw_response = completion.choices[0].message.parsed

        # Ensure the response is in the correct format for FastAPI
        questions = raw_response.questions
        suggested_answers = raw_response.suggested_answers

        # If no questions were generated, log and return empty lists
        if not questions or not suggested_answers:
            print("No questions or suggested answers were generated.")
            return {"questions": [], "suggested_answers": []}

        return {"questions": questions, "suggested_answers": suggested_answers}

    except Exception as e:
        print(f"Error generating questions: {e}")
        return {"questions": [], "suggested_answers": []}