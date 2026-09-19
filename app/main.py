from fastapi import FastAPI
from app.database.connection import engine, Base
from app.models.student import Student
from app.routers.students import router as student_router


app = FastAPI(
    title="Student Database API",
    description="Backend API for Student Database Application System",
    version="1.0.0"
)


app.include_router(student_router)


Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Student Database API is running"
    }
