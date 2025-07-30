from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
    major: str
    year: int
    gpa: float = 0.0

class Course(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    professor_id: int
    max_capacity: int

class Professor(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    hire_date: date

class Enrollment(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
    grade: Optional[float] = None
