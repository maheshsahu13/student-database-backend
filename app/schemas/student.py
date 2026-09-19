from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = None
    department: str = Field(..., min_length=2, max_length=100)
    course: str = Field(..., min_length=2, max_length=100)
    semester: int = Field(..., ge=1, le=8)
    cgpa: float | None = Field(None, ge=0, le=10)


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    department: str | None = None
    course: str | None = None
    semester: int | None = Field(None, ge=1, le=8)
    cgpa: float | None = Field(None, ge=0, le=10)