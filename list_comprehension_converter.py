# Convert traditional for-loop-based list creation into list comprehensions. Include examples with:

# Simple list creation
# Filtering conditions (e.g., only even numbers)
# Nested loops (e.g., combinations or matrix flattening)


listofnumbers = [x for x in range(1, 11)]

listofEvens = [x for x in range(1, 11) if x % 2 == 0]

nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

flattened_list = [item for sublist in nested_list for item in sublist]