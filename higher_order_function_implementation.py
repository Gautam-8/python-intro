

def custom_map(iterable, func) : 
    return [func(x) for x in iterable]

def custom_filter(func, iterable):
    return [x for x in iterable if func(x)]

def custom_reduce(func, iterable):
    res = iterable[0]
    for x in iterable[1:] :
        res = func(res, x)
    return res
