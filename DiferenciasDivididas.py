from sympy import *

f1 = "-2,-1,2,3"
f1 = eval("["+f1+"]")

f2 = "4,1,4,9"
f2 = eval("["+f2+"]")

n = len(f1)
#n = int(input("Ingrese el grado del polinomio a evaluar: ")) + 1

matriz = [0.0] * n

for i in range(n):
    matriz[i] = [0.0] * n

vector = [0.0] * n

print(matriz)
print(vector)

for i in range(n):
    #x = input("Ingrese el valor de x: ")
    #y = input("Ingrese el valor de f("+x+"): ")
    vector[i]=float(f1[i])
    matriz[i][0]=float(f2[i])

print(vector)    
print(matriz)

punto_a_evaluar = float(input("Ingrese el punto a evaluar: "))

for i in range(1,n):
    for j in range(i,n):
        print ("i = ",i,"    j = ",j)
        print ("(",matriz[j][i-1],"-",matriz[j-1][i-1],")/(",vector[j],"-",vector[j-i],")")
        matriz[j][i] = ( (matriz[j][i-1]-matriz[j-1][i-1]) / (vector[j]-vector[j-i]))
        print ("matriz[",j,"][",i,"] = ",(matriz[j][i-1]-matriz[j-1][i-1])/(vector[j]-vector[j-i]))

contador = 0
formula = ""

for i in range(n):
    formula += "(" + str(matriz[i][i])
    for j in range(contador):
        formula += "*" + "(x-("+ str(vector[j]) + "))"
    formula += ")"
    formula += "+" if i < n - 1 else ""

    contador = contador + 1
    print (matriz[i])

print(formula)


formula = solve("-y+"+formula, "y")
print(formula[0])

aprx = 0
mul = 1.0
for i in range(n):
    mul = matriz[i][i]
    for j in range(1,i+1):
        mul = mul * (punto_a_evaluar - vector[j-1])
    aprx = aprx + mul

print ("El valor aproximado de f(",punto_a_evaluar,") es: ", aprx)