from functools import reduce

arr = [1,2,3,4,5]

square = lambda x : x**2
factoriall = lambda arr: reduce(lambda a, b : a*b, arr)

reverse = lambda x:x[::-1]
uppers = lambda word : word.upper()

filter_evens = lambda lst: list(filter(lambda X:X%2 == 0, lst))
sum = lambda arr : reduce(lambda a,b : a+b, arr)

