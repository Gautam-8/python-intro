a = [1, 2, 3]
b = [4, 5, 6]

dot_product = lambda a,b : sum([x * y for x,y in zip(a,b)])
dot_product_val = dot_product(a,b)
print(dot_product_val)
print("Orthogonal -> ", dot_product_val == 0)
sum_vector = lambda a,b : [x + y for x,y in zip(a,b)]
print(sum_vector(a,b))


A = [
[1, 2], 
[3, 4]
]

B = [
[5, 6], 
[7, 8]]

res = []

for idx, lst in enumerate(A):
    r = [] 
    for i in range(len(B[0])) :
        r.append(sum( [ x*B[j][i] for j,x in enumerate(A[idx]) ] ))
    res.append(r)

print(res)