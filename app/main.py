from fastapi import FastAPI
from app.database.connection import engine, Base
from app.models.student import Student
from app.models.user import User
from app.routers.students import router as student_router
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router


app = FastAPI(
    title="Student Database API",
    description="REST API for managing student records.",
    version="1.0.0"
)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "student-database-api"
    }


app.include_router(student_router)
app.include_router(auth_router)
app.include_router(chat_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Student Database API is running"
    }
