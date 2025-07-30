from fastapi import APIRouter, HTTPException
from models import Enrollment
from db import enrollments, students, courses
from logic import calculate_gpa

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.get("/")
def get_enrollments():
    return enrollments

@router.post("/")
def enroll_student(enroll: Enrollment):
    if enroll.student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if enroll.course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    course = courses[enroll.course_id]
    enrolled_count = len([e for e in enrollments if e["course_id"] == enroll.course_id])
    if enrolled_count >= course["max_capacity"]:
        raise HTTPException(status_code=400, detail="Course is full")

    for e in enrollments:
        if e["student_id"] == enroll.student_id and e["course_id"] == enroll.course_id:
            raise HTTPException(status_code=400, detail="Student already enrolled")

    enrollments.append(enroll.dict())
    return enroll

@router.put("/{student_id}/{course_id}")
def update_grade(student_id: int, course_id: int, grade: float):
    for e in enrollments:
        if e["student_id"] == student_id and e["course_id"] == course_id:
            e["grade"] = grade
            # Update GPA
            student_courses = [en for en in enrollments if en["student_id"] == student_id]
            students[student_id]["gpa"] = calculate_gpa(student_courses)
            return {"message": "Grade updated and GPA recalculated"}
    raise HTTPException(status_code=404, detail="Enrollment not found")

@router.delete("/{student_id}/{course_id}")
def drop_course(student_id: int, course_id: int):
    global enrollments
    enrollments = [e for e in enrollments if not (e["student_id"] == student_id and e["course_id"] == course_id)]
    return {"message": "Course dropped"}
