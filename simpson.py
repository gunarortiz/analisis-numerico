from sympy import *
from mpmath import *
mp.pretty = True


def formulaIntro(x, formula):
    solucion = solve("-y+" + formula, "y")
    solucion = eval(str(solucion[0]))

    print(solucion)
    return solucion



formula = str(input("inserte formula"))
nodos = int(input("nodos"))

a=float(input("inserte a"))
b=float(input("inserte b"))

m=int(nodos/2)

h=float((b-a)/(2*m))

solucion = float(h/3*(formulaIntro(a, formula) + formulaIntro(b, formula)))

par = 0
impar = 0

for i in range(1, (2*m)):
    xs = a + (i * h)
    print("X" + str(i) + ":" + str(xs))
    xs = formulaIntro(xs, formula)
    if i%2 == 0:
        par += xs
    else:
        impar += xs


solucion+=float(((2*h)/3) * par + ((4*h)/3) * impar )
print(solucion)

