from app.database.connection import SessionLocal
from app.crud.student import get_students
from app.config.settings import GEMINI_API_KEY
from app.services.retrieval_service import RetrievalService
from langchain_google_genai import ChatGoogleGenerativeAI


model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GEMINI_API_KEY
)

retrieval_service = RetrievalService()


def classify_question(state):
    question = state.get("question", "").lower()

    structured_keywords = [
        "highest cgpa",
        "lowest cgpa",
        "maximum cgpa",
        "minimum cgpa",
        "cgpa above",
        "cgpa below",
        "cgpa greater",
        "cgpa less",
        "cgpa greater than",
        "cgpa less than",
        "how many students",
        "total students",
        "count students",
        "highest",
        "lowest",
        "maximum",
        "minimum",
        "greater than",
        "less than",
    ]

    semantic_keywords = [
        "studying",
        "study",
        "similar",
        "strong academic",
        "academic performance",
        "students like",
        "student like",
        "background",
        "profile",
        "related to",
        "interested",
    ]

    has_structured = any(
        keyword in question
        for keyword in structured_keywords
    )

    has_semantic = any(
        keyword in question
        for keyword in semantic_keywords
    )

    if has_structured and has_semantic:
        retrieval_type = "hybrid"

    elif has_structured:
        retrieval_type = "structured"

    elif has_semantic:
        retrieval_type = "semantic"

    else:
        retrieval_type = "semantic"

    return {
        **state,
        "retrieval_type": retrieval_type
    }
def extract_filters(question):
    question_lower = question.lower()

    filters = {
        "department": None,
        "cgpa_operator": None,
        "cgpa_value": None
    }

    # Detect department
    departments = [
        "cse",
        "computer science",
        "ece",
        "electrical",
        "mechanical",
        "civil",
        "ai",
        "artificial intelligence"
    ]

    for department in departments:
        if department in question_lower:
            filters["department"] = department
            break

    # Detect CGPA comparison
    import re

    cgpa_patterns = [
        (r"cgpa\s+(?:above|greater than|more than)\s+(\d+(?:\.\d+)?)", ">"),
        (r"cgpa\s+(?:below|less than)\s+(\d+(?:\.\d+)?)", "<"),
        (r"cgpa\s+(?:equal to|equals)\s+(\d+(?:\.\d+)?)", "="),
    ]

    for pattern, operator in cgpa_patterns:
        match = re.search(pattern, question_lower)

        if match:
            filters["cgpa_operator"] = operator
            filters["cgpa_value"] = float(match.group(1))
            break

    return filters

def get_structured_students(question=None):
    db = SessionLocal()

    try:
        students = get_students(db)

        if question:
            filters = extract_filters(question)

            department = filters["department"]
            cgpa_operator = filters["cgpa_operator"]
            cgpa_value = filters["cgpa_value"]

            # Department filtering
            if department:
                if department == "computer science":
                    students = [
                        student for student in students
                        if "computer" in student.department.lower()
                        or student.department.lower() == "cse"
                    ]
                elif department == "artificial intelligence":
                    students = [
                        student for student in students
                        if "artificial intelligence" in student.department.lower()
                        or student.department.lower() == "ai"
                    ]
                else:
                    students = [
                        student for student in students
                        if student.department.lower() == department
                    ]

            # CGPA filtering
            if cgpa_operator and cgpa_value is not None:

                if cgpa_operator == ">":
                    students = [
                        student for student in students
                        if student.cgpa is not None
                        and student.cgpa > cgpa_value
                    ]

                elif cgpa_operator == "<":
                    students = [
                        student for student in students
                        if student.cgpa is not None
                        and student.cgpa < cgpa_value
                    ]

                elif cgpa_operator == "=":
                    students = [
                        student for student in students
                        if student.cgpa is not None
                        and student.cgpa == cgpa_value
                    ]

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

        return student_data

    finally:
        db.close()
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

        return student_data

    finally:
        db.close()


def get_semantic_students(question):
    results = retrieval_service.semantic_search(
        query=question,
        n_results=5
    )

    student_data = []

    for result in results:
        student_data.append({
            "document": result["document"],
            "metadata": result["metadata"],
            "distance": result["distance"]
        })

    return student_data


def retrieve_students(state):
    retrieval_type = state.get(
        "retrieval_type",
        "semantic"
    )

    question = state.get("question", "")

    if retrieval_type == "structured":
        students = get_structured_students(question)

        return {
            **state,
            "students": students
        }

    if retrieval_type == "semantic":
        students = get_semantic_students(question)

        return {
            **state,
            "students": students
        }

    structured_students = get_structured_students(question)
    semantic_students = get_semantic_students(question)

    return {
        **state,
        "students": structured_students,
        "semantic_students": semantic_students
    }


def generate_answer(state):
    question = state.get("question", "")
    students = state.get("students", [])
    semantic_students = state.get(
        "semantic_students",
        []
    )
    retrieval_type = state.get(
        "retrieval_type",
        "semantic"
    )

    prompt = f"""
You are an assistant for a student database application.

Answer the user's question using ONLY the student
information provided below.

Retrieval type:
{retrieval_type}

Structured student database:
{students}

Semantic search results:
{semantic_students}

User question:
{question}

Rules:

- Use only the provided student information.
- Never invent student information.
- SQLite/structured data is the source of truth for
  exact values such as CGPA, semester, department,
  course, and student count.
- Semantic search results are used to understand
  conceptual or natural-language relationships.
- For hybrid questions, combine the structured data
  with the semantic results.
- For exact numerical questions, calculate using the
  actual provided values.
- If the requested information is not available,
  clearly say that it is not available.
- Keep the answer clear and concise.
"""

    response = model.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        answer = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "text"
        )
    else:
        answer = str(content)

    return {
        **state,
        "answer": answer
    }