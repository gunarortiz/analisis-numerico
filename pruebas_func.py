import sympy as sym
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
from sympy.utilities import lambdify
import re

"""transformations = (standard_transformations + (implicit_multiplication_application,))

x = sym.Symbol('x')
in_str = ''
for ch in input():
    if ch == '^':
        in_str += '**'
    else:
        in_str += ch

print(in_str)

f = parse_expr(in_str, transformations=transformations)
f = lambdify((x), f)

print(f(int(input())))"""

def despejar(func):
    func = func.replace(' ','')
    expr = func.split('=')
    print(expr)
    operators = []
    for (i,ch) in enumerate(expr[1]):
        #print(i,ch)
        if ch in ['+','-','*','/']:
            operators.append(())

    if len(operators) == 0:
        func = expr[0] + '-' + expr[1]
    else:
        coeffs = re.split('-|\+|\*|/|\^|=',expr[1])
        print(coeffs)

    return func

#str = input()
str = 'x^2 = 2^x + 2'
print(despejar(str))
print()

def prepocess_input(inp):
    in_str = ''
    res_str = ''
    inp = inp.replace(' ','')
    decomp = inp.split('e')
    #print(decomp)
    for v in decomp:
        if v[0] == 'x' and v[1] == 'p':
            # print(True)
            res_str = res_str + 'e' + v
        else:
            # print(False)
            if v[0] == '^':
                res_str = res_str + 'exp' + v
            else:
                res_str += v
    #print(decomp)
    #print(res_str)

    for ch in res_str:
        if ch == '^':
            in_str += '**'
        else:
            in_str += ch

    return in_str

str = '-3x^2 + exp^(3x) + e^x - 2'
print(prepocess_input(str)[1:])
"""str = str.replace(' ','')
decomp = str.split('e')
res_str = ''
for v in decomp:
    if v[0] == 'x':
        #print(True)
        res_str = res_str + 'e' + v
    else:
        #print(False)
        if v[0] == '^':
            res_str = res_str + 'exp' + v
        else:
            res_str += v
print(decomp)
print(res_str)"""


#str = 'x^2=2^x-3x+25*54x/6'
#print(re.split('-|\+|\*|/|\^|=', str))