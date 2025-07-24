school = {
    "Math": {
        "teacher": "Mr. Smith",
        "students": [("Alice", 85), ("Bob", 92), ("Carol", 78)]
    },
    "Science": {
        "teacher": "Ms. Johnson",
        "students": [("David", 88), ("Eve", 94), ("Frank", 82)]
    }
}

print("Teachers:")
for subject, details in school.items():
    print(f"{subject}: {details['teacher']}")

for subject, details in school.items():
    total = sum(grade for _, grade in details['students'])
    count = len(details['students'])
    avg = total / count
    print(f"{subject}: {avg:.2f}")

top_student = ("", 0)
for details in school.values():
    for name, grade in details['students']:
        if grade > top_student[1]:
            top_student = (name, grade)

print(f"{top_student[0]} ({top_student[1]})")
