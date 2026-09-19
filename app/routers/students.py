from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.crud.student import create_student, get_students, get_student, update_student, delete_student


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


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
        return create_student(db, student)

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[StudentResponse],
    summary="Get students",
    description="Get all students or filter students by department and course."
)
def read_students(
    department: str | None = None,
    course: str | None = None,
    db: Session = Depends(get_db)
):
    return get_students(db, department, course)

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

    return student