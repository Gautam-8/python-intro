grades = [85, 92, 78, 90, 88, 76, 94, 89, 87, 91]

sliced = grades[2:8]
print("Sliced (index 2 to 7):", sliced)

above_85 = [grade for grade in grades if grade > 85]
print("Grades above 85:", above_85)


grades[3] = 95
print("After replacing index 3 with 95:", grades)


grades.extend([82, 96, 88])
print("After appending new grades:", grades)


top_5 = sorted(grades, reverse=True)[:5]
print("Top 5 grades (descending):", top_5)
