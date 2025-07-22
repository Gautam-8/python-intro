from functools import reduce


arr = [1, 2, 3, 4, 5, 6]

sum = reduce(lambda a,b : a +b, arr)
print(sum)

squares = list(map(lambda x: x**2, arr))
print(squares)

evens = list(filter(lambda x: x % 2 == 0, arr))
print(evens)

unique = list(set([1, 1, 2, 2, 3]))
print(unique)

palindromes = list(filter(lambda w: w == w[::-1], ["madam", "hello", "noon", "racecar", "python"]))
print(palindromes)

