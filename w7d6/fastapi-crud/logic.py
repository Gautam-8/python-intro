def calculate_gpa(student_enrollments):
    grades = [e['grade'] for e in student_enrollments if e.get('grade') is not None]
    if not grades:
        return 0.0
    return round(sum(grades) / len(grades), 2)
