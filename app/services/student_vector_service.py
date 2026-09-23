from app.models.student import Student
from app.services.vector_store import VectorStore


class StudentVectorService:
    def __init__(self):
        self.vector_store = VectorStore()

    def create_student_text(self, student: Student) -> str:
        return (
            f"Student name: {student.name}. "
            f"Email: {student.email}. "
            f"Department: {student.department}. "
            f"Course: {student.course}. "
            f"Semester: {student.semester}. "
            f"CGPA: {student.cgpa}."
        )

    def index_student(self, student: Student):
        text = self.create_student_text(student)

        metadata = {
            "student_id": student.id,
            "name": student.name,
            "department": student.department,
            "course": student.course,
            "semester": student.semester,
            "cgpa": student.cgpa if student.cgpa is not None else 0.0,
        }

        self.vector_store.add_student(
            student_id=student.id,
            text=text,
            metadata=metadata,
        )