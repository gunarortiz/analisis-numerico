import math

def sec(x_0, x_1, iters, f, tol, eps):
    x_i0 = x_0
    x_i1 = x_1
    for i in range(iters):
        temp = (x_i0*f(x_i1) - x_i1*f(x_i0))/(f(x_i1)-f(x_i0) + eps)
        print(temp)
        x_i0 = x_i1
        x_i1 = temp

    return x_i1

func = lambda x: math.cos(x) - x**2 + 1
tol = 0.0005

x_0, x_1 = 1, 2
res = sec(x_0, x_1, 6, func, tol, eps=1e-16)
print(res, func(res))