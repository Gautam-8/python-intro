from fastapi import APIRouter, HTTPException
from models import Student
from db import students, enrollments

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
def get_students():
    return list(students.values())

@router.get("/{student_id}")
def get_student(student_id: int):
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/")
def create_student(student: Student):
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student already exists")
    students[student.id] = student.dict()
    return student

@router.put("/{student_id}")
def update_student(student_id: int, updated: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = updated.dict()
    return updated

@router.delete("/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted"}

@router.get("/{student_id}/courses")
def get_student_courses(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    student_courses = [e for e in enrollments if e["student_id"] == student_id]
    return student_courses
