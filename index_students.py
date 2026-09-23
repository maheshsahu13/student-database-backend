from dotenv import load_dotenv

load_dotenv()

from app.database.connection import SessionLocal
from app.models.student import Student
from app.services.student_vector_service import StudentVectorService


db = SessionLocal()

try:
    students = db.query(Student).all()

    print(f"Found {len(students)} students in SQLite.")

    vector_service = StudentVectorService()

    for student in students:
        vector_service.index_student(student)

        print(
            f"Indexed: {student.name} "
            f"(ID: {student.id})"
        )

    print("\nAll students indexed successfully!")

finally:
    db.close()