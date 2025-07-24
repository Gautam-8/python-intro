employees = [
    ("Alice", 70000, "Engineering"),
    ("Bob", 50000, "HR"),
    ("Charlie", 60000, "Engineering"),
    ("David", 55000, "Marketing"),
    ("Eve", 75000, "Marketing")
]


# Ascending
by_salary_asc = sorted(employees, key=lambda x: x[1])
print("Sorted by salary (ascending):", by_salary_asc)

# Descending
by_salary_desc = sorted(employees, key=lambda x: x[1], reverse=True)
print("Sorted by salary (descending):", by_salary_desc)


by_dept_then_salary = sorted(employees, key=lambda x: (x[2], x[1]))
print("Sorted by department, then salary:", by_dept_then_salary)


reversed_list = employees[::-1]
print("Reversed list (original unchanged):", reversed_list)


by_name_length = sorted(employees, key=lambda x: len(x[0]))
print("Sorted by name length:", by_name_length)

# Make a copy to preserve original
employees_copy = employees.copy()

# In-place sort by salary
employees_copy.sort(key=lambda x: x[1])
print("In-place sort by salary using .sort():", employees_copy)

