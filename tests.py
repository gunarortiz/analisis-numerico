import sympy as sym
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
import math
import matplotlib.pyplot as plt

from fractions import Fraction

def solve_math_errors(f, a, eps):
    sw = False
    while sw == False:
        try:
            f((a-1)+eps)
            sw = True
        except ValueError:
            a += 1
    return a

def intersecciones(f, a, b, eps):
    xs, ys = [],[]
    intersect = []

    a = solve_math_errors(f, a, eps)

    prev = f((a-1)+eps)
    for x_i in range(a,b+1):
        xs.append(x_i)

        act = f(x_i+eps)
        ys.append(act)
        if act*prev <= 0 + eps:
            intersect.append((x_i - 1 + eps, x_i + eps))
        prev = act

    plt.plot(xs,ys)
    plt.show()

    return intersect

def mostrar_tabla(table):
    for (i, row) in enumerate(table):
        print('[' + str(i + 1) + ']', row)

def biseccion(a, b, its, f):
    a_orig, b_orig = a,b
    sw = False
    c = 0
    while sw == False and c < 2:
        table = [[] for i in range(its)]
        for it in range(its):
            if it %200 == 0:
                print(it)
            X_m = ((a) + (b)) / 2

            res = (X_m)

            im_a, im_b, im_X_m = f((a),a_orig,b_orig), f((b),a_orig,b_orig), f((X_m),a_orig,b_orig)

            table[it] = [str((a)) + (' ^+' if im_a > 0 else ' ^-'),
                         str((b)) + (' ^+' if im_b > 0 else ' ^-'),
                         str((X_m)) + (' ^+' if im_X_m > 0 else ' ^-')]

            if im_X_m > 0:
                b = (X_m)
            else:
                a = (X_m)

        if abs(round((f(res,a_orig,b_orig)),2)) <= round((0.1),2):
            sw = True
        else:
            b = a_orig
            a = b_orig
        c += 1

        print(mostrar_tabla(table))
        print()
    return (res), (True if (f(res,a_orig,b_orig) == 0) else False)

#4.17
x_t = sym.Symbol('x')
f_p =  x_t**3 - 2*sym.cos(x_t) - 3
func = lambda z,x,alpha: f_p.evalf(subs={x_t:x}) + sym.diff(f_p.evalf(subs={x_t:x}),x_t)*(alpha - x) + (1/2)*(alpha - x)**2*sym.diff(f_p.evalf(subs={x_t:z}),x_t,2) - f_p.evalf(subs={x_t:alpha})

print(biseccion(math.pi/4,1,10,func)[0])