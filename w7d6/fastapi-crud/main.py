from fastapi import FastAPI
from routers import students, courses, professors, enrollments

app = FastAPI(title="University Course Management System")

app.include_router(students.router)
app.include_router(courses.router)
app.include_router(professors.router)
app.include_router(enrollments.router)

@app.get("/")
def root():
    return {"message": "University API is running!"}
