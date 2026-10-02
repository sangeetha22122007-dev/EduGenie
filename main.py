import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing in .env file")


# Gemini client
client = genai.Client(api_key=API_KEY)

# FastAPI application
app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0"
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Request model
class UserRequest(BaseModel):
    text: str


def ask_gemini(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini API Error: {str(e)}"
        )


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {
        "status": "running",
        "project": "EduGenie"
    }


@app.post("/ask")
def ask_question(request: UserRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    prompt = f"""
You are EduGenie, an AI educational assistant.

Answer the student's question clearly and accurately.

Rules:
- Use simple English.
- Explain difficult concepts in an easy way.
- Give examples when useful.
- Keep the answer student-friendly.

Student Question:
{request.text}
"""

    answer = ask_gemini(prompt)

    return {
        "type": "answer",
        "result": answer
    }


@app.post("/quiz")
def generate_quiz(request: UserRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a topic."
        )

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create a quiz for the topic below.

Topic:
{request.text}

Create:
- 5 multiple-choice questions
- 4 options for each question
- Clearly mention the correct answer
- Give a short explanation for each answer
- Suitable for college students
"""

    result = ask_gemini(prompt)

    return {
        "type": "quiz",
        "result": result
    }


@app.post("/summarize")
def summarize_text(request: UserRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter text to summarize."
        )

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational text.

Requirements:
- Keep the important points.
- Use simple English.
- Use bullet points.
- Make it easy for students to study.

Text:
{request.text}
"""

    result = ask_gemini(prompt)

    return {
        "type": "summary",
        "result": result
    }


@app.post("/learning-path")
def learning_path(request: UserRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a subject."
        )

    prompt = f"""
You are EduGenie, a personalized learning path generator.

Create a structured learning plan for:

Subject:
{request.text}

Include:
1. Beginner topics
2. Intermediate topics
3. Advanced topics
4. Suggested timeline
5. Practice activities
6. Project ideas
7. Useful learning tips

Make it suitable for a college student.
"""

    result = ask_gemini(prompt)

    return {
        "type": "learning_path",
        "result": result
    }