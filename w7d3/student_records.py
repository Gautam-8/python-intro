from tracemalloc import get_traced_memory


students = [
    (101, "Alice", 85, 20),
    (102, "Bob", 92, 19),
    (103, "Caarol", 78, 21),
    (104, "David", 88, 20)
]

highest = max([grade for _,_,grade,_ in students])
print(highest)
gradeTuple = [(name, grade) for _,name,grade,_ in students]
print(gradeTuple)
students[0][2] = 98