from app.database.connection import SessionLocal
from app.crud.student import get_students
from app.config.settings import GEMINI_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI


model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GEMINI_API_KEY
)


def retrieve_students(state):
    db = SessionLocal()

    try:
        students = get_students(db)

        student_data = []

        for student in students:
            student_data.append({
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "phone": student.phone,
                "department": student.department,
                "course": student.course,
                "semester": student.semester,
                "cgpa": student.cgpa
            })

        return {
            **state,
            "students": student_data
        }

    finally:
        db.close()


def generate_answer(state):
    question = state.get("question", "")
    students = state.get("students", [])

    prompt = f"""
You are an assistant for a student database application.

Answer the user's question using the student database information provided below.

Student database:
{students}

User question:
{question}

Rules:
- Use the database information when answering.
- Do not invent student information.
- If the requested information is not present, clearly say that it is not available.
- Keep the answer clear and concise.
"""

    response = model.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        answer = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        )
    else:
        answer = str(content)

    return {
        **state,
        "answer": answer
    }