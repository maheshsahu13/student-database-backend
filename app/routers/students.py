from fastapi import APIRouter, Depends, HTTPException, Query
from app.security.auth import get_current_user
from typing import Literal
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.crud.student import (
    create_student,
    get_students,
    get_student,
    update_student,
    delete_student
)

from app.services.student_vector_service import StudentVectorService


router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)]
)


# Create vector service once for this router
vector_service = StudentVectorService()


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=201,
    summary="Create a student",
    description="Create a new student. The email address must be unique."
)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    try:
        new_student = create_student(db, student)

        # Sync the newly created student with ChromaDB
        vector_service.index_student(new_student)

        return new_student

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[StudentResponse],
    summary="Get students",
    description="Get all students or filter students by department and course with pagination."
)
def read_students(
    department: str | None = None,
    course: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort_by: Literal["id", "name", "email"] = "id",
    sort_order: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db)
):
    students = get_students(db, department, course)

    if sort_by == "name":
        students.sort(key=lambda student: student.name.lower())
    elif sort_by == "email":
        students.sort(key=lambda student: student.email.lower())
    else:
        students.sort(key=lambda student: student.id)

    if sort_order.lower() == "desc":
        students.reverse()

    start = (page - 1) * limit
    end = start + limit

    return students[start:end]


@router.get(
    "/stats",
    summary="Get student statistics",
    description="Get summary statistics about students."
)
def get_student_stats(
    db: Session = Depends(get_db)
):
    students = get_students(db, None, None)

    total_students = len(students)
    total_departments = len(
        set(student.department for student in students)
    )
    total_courses = len(
        set(student.course for student in students)
    )

    department_counts = {}

    for student in students:
        department_counts[student.department] = (
            department_counts.get(student.department, 0) + 1
        )

    return {
        "total_students": total_students,
        "total_departments": total_departments,
        "total_courses": total_courses,
        "students_by_department": department_counts
    }


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get student by ID",
    description="Get the details of a single student using their student ID."
)
def read_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    return student


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update student",
    description="Update the details of an existing student using their student ID."
)
def edit_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = update_student(db, student_id, student_data)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    # Sync the updated student with ChromaDB
    vector_service.index_student(student)

    return student


@router.delete(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Delete student",
    description="Delete an existing student using their student ID."
)
def remove_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = delete_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found"
        )

    # Remove the deleted student from ChromaDB
    vector_service.vector_store.collection.delete(
        ids=[str(student_id)]
    )

    return student