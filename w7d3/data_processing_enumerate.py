students = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']
scores = [85, 92, 88, 95, 70]

print("Numbered List of Students:")
for idx, name in enumerate(students, start=1):
    print(f"{idx}. {name}")

print("\nStudents with Scores:")
for idx, (name, score) in enumerate(zip(students, scores)):
    print(f"{idx}. {name} - {score}")

high_scorers_indices = [idx for idx, score in enumerate(scores) if score > 90]
print("\nPositions of High Scorers (score > 90):", high_scorers_indices)

position_to_name = {idx: name for idx, name in enumerate(students)}
print("\nPosition to Student Name Mapping:")
print(position_to_name)
