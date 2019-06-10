from sympy import *
from mpmath import *

var: str = 'sin(3)+3*x'

formula = solve("-y+"+var, "y")

x=3
mp.pretty = True

print(str(eval(str(formula))[0]))