func = lambda x, P: (P/x**2 + 2*x)/3

def cubic_root(p, its, x_0 = 1):
    x_i = x_0
    for i in range(its):
        x_i = func(x_i, p)
        #print(x_i)

    return x_i

res = cubic_root(p = 100, its = 10)
print(res)

res = cubic_root(p = 53701, its = 100)
print(res)

res = cubic_root(p = 19.35, its = 10)
print(res)