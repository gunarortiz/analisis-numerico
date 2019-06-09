import sympy as sym
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
from sympy.utilities import lambdify
import math
import matplotlib.pyplot as plt
from scipy.misc import derivative

from fractions import Fraction
from decimal import *

getcontext().prec = 30

def prepocess_input():
    in_str = ''
    for ch in input():
        if ch == '^':
            in_str += '**'
        else:
            in_str += ch

    return in_str

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


def iterando(a, b, X_0, its, table, f):
    res = X_0

    for i in range(its):
        res = res - (f(res) / derivative(f, res, dx=1e-10))
        # res = res - ( f(res) / dx(res) )
        table[i] = res

    return res

def biseccion(a, b, its, f, print_vals = True):
    a_orig, b_orig = a,b
    sw = False

    im_X_m = a_orig
    while sw == False:
        table = [[] for i in range(its)]
        for it in range(its):

            X_m = (a + b) / 2

            res = X_m

            im_a, im_b, im_X_m = f(a), f(b), f(X_m)

            table[it] = [str(Fraction(a)) + (' ^+' if im_a > 0 else ' ^-'),
                         str(Fraction(b)) + (' ^+' if im_b > 0 else ' ^-'),
                         str(Fraction(X_m)) + (' ^+' if im_X_m > 0 else ' ^-')]

            if im_X_m > 0:
                b = X_m
            else:
                a = X_m

        if abs(round(f(res),2)) <= round(0.1,2):
            sw = True
        else:
            b = a_orig
            a = b_orig

    return res, (True if (f(res) == 0) else False), sw

if __name__ == "__main__":

    transformations = (standard_transformations + (implicit_multiplication_application,))


    #4.16
    #func = lambda x: (x - 1)**2
    #4.18
    #func = lambda x: -1536 + 6272*x - 11328*x**2 + 11872*x**3 - 7952*x**4 + 3528*x**5 - 1036*x**6 + 194*x**7 - 21*x**8 + x**9
    #4.19
    #func = lambda x: 2 - 19*x + 81*x**2 - 204*x**3 + 336*x**4 -378*x**5 + 294*x**6 - 156*x**7 + 54*x**8 - 11*x**9 + x**10
    #func = lambda x: (x-1)**2
    func = lambda x: math.cos(x) - x**2 + 1
    #func = lambda x: x*math.exp(-x) - 0.2

    #bronsten
    #func = lambda x: x**3+0.00001905*x**2-0.000000000001915*x-0.0000000000000000001905
    #func = lambda x: math.exp(3*x)-math.log(x**2+1)-30
    """X = sym.Symbol('x')
    func = parse_expr(prepocess_input(), transformations=transformations)
    func = lambdify((X), func)"""

    intersect = intersecciones(func, -50, 50, 1e-8)
    print(intersect)

    for e in intersect:
        res, sw, sw1 = biseccion(e[0],e[1], 10000, func)
        #table = [[] for i in range(100)]
        #res = iterando(e[0], e[1], e[0], 10, table, func)
        print(res,'->', abs(round(func(res),2)), sw1)
    print(biseccion(0, 1, 1000, func))
    print(biseccion(3, 2, 1000, func, print_vals = True))

#x = Symbol('x')
#func = lambda x: x**2 - 2**x
#func = parse_expr(input(), transformations=transformations)
#print(func)
#print(diff(func))
#print(func.evalf(subs={x:3}))


#func = lambda x: x**3 + 4*x**2 - 1
#func = lambda x: math.exp(3*x) - math.log(x - 1)**2 + 1
#func = lambda x: math.exp(3 * x) - math.log(x**2 + 1) ** 2 - 30


"""
def biseccion(a, b, its, f):
    a_orig, b_orig = a,b
    sw = False

    im_X_m = a_orig
    while sw == False:
        table = [[] for i in range(its)]
        for it in range(its):

            X_m = (Decimal(a) + Decimal(b)) / 2

            res = Decimal(X_m)

            im_a, im_b, im_X_m = f(Decimal(a)), f(Decimal(b)), f(Decimal(X_m))

            table[it] = [str(Fraction(a)) + (' ^+' if im_a > 0 else ' ^-'),
                         str(Fraction(b)) + (' ^+' if im_b > 0 else ' ^-'),
                         str(Fraction(X_m)) + (' ^+' if im_X_m > 0 else ' ^-')]

            if Decimal(im_X_m) > 0:
                b = Decimal(X_m)
            else:
                a = Decimal(X_m)

        if abs(round(Decimal(f(res)),2)) <= round(Decimal(0.1),2):
            sw = True
        else:
            b = a_orig
            a = b_orig

    return Decimal(res), (True if (f(Decimal(res)) == 0) else False)
"""