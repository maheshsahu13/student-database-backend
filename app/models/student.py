from sqlalchemy import Column, Integer, String, Float
from app.database.connection import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    department = Column(String, nullable=False)
    course = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    cgpa = Column(Float, nullable=True)