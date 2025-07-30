from fastapi import APIRouter, HTTPException
from models import Professor
from db import professors, courses

router = APIRouter(prefix="/professors", tags=["Professors"])

@router.get("/")
def get_professors():
    return list(professors.values())

@router.get("/{professor_id}")
def get_professor(professor_id: int):
    prof = professors.get(professor_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    return prof

@router.post("/")
def create_professor(prof: Professor):
    if prof.id in professors:
        raise HTTPException(status_code=400, detail="Professor already exists")
    professors[prof.id] = prof.dict()
    return prof

@router.put("/{professor_id}")
def update_professor(professor_id: int, updated: Professor):
    if professor_id not in professors:
        raise HTTPException(status_code=404, detail="Professor not found")
    professors[professor_id] = updated.dict()
    return updated

@router.delete("/{professor_id}")
def delete_professor(professor_id: int):
    if professor_id not in professors:
        raise HTTPException(status_code=404, detail="Professor not found")
    del professors[professor_id]
    return {"message": "Professor deleted"}

@router.get("/{professor_id}/courses")
def get_professor_courses(professor_id: int):
    return [course for course in courses.values() if course["professor_id"] == professor_id]
