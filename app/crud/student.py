from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


def create_student(db: Session, student: StudentCreate):
    db_student = Student(
        name=student.name,
        email=student.email,
        phone=student.phone,
        department=student.department,
        course=student.course,
        semester=student.semester,
        cgpa=student.cgpa
    )

    db.add(db_student)

    try:
        db.commit()
        db.refresh(db_student)

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists")

    return db_student


def get_students(db: Session, department=None, course=None):
    query = db.query(Student)

    if department:
        query = query.filter(Student.department == department)

    if course:
        query = query.filter(Student.course == course)

    return query.all()

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def update_student(db: Session, student_id: int, student_data: StudentUpdate):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if db_student is None:
        return None

    update_data = student_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    return db_student


def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if db_student is None:
        return None

    db.delete(db_student)
    db.commit()

    return db_student