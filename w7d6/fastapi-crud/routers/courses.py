from fastapi import APIRouter, HTTPException
from models import Course
from db import courses, professors, enrollments

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/")
def get_courses():
    return list(courses.values())

@router.get("/{course_id}")
def get_course(course_id: int):
    course = courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/")
def create_course(course: Course):
    if course.id in courses:
        raise HTTPException(status_code=400, detail="Course already exists")
    if course.professor_id not in professors:
        raise HTTPException(status_code=400, detail="Professor not found")
    courses[course.id] = course.dict()
    return course

@router.put("/{course_id}")
def update_course(course_id: int, updated: Course):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    courses[course_id] = updated.dict()
    return updated

@router.delete("/{course_id}")
def delete_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]
    return {"message": "Course deleted"}

@router.get("/{course_id}/students")
def get_course_students(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return [e for e in enrollments if e["course_id"] == course_id]
