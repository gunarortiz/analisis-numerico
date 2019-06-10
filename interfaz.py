import tkinter as tk
#import sympy as sym
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
from sympy.utilities import lambdify
from fractions import Fraction

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import numpy as np

from mpmath import *
mp.pretty = True

from scipy.misc import derivative


def diferencias(primer_campo, segundo_campo, tercer_campo):
    f1 = primer_campo
    f1 = eval("[" + f1 + "]")

    f2 = segundo_campo
    f2 = eval("[" + f2 + "]")

    n = len(f1)

    matriz = [0.0] * n

    for i in range(n):
        matriz[i] = [0.0] * n

    vector = [0.0] * n

    print(matriz)
    print(vector)

    for i in range(n):
        vector[i] = float(f1[i])
        matriz[i][0] = float(f2[i])

    print(vector)
    print(matriz)

    punto_a_evaluar = float(tercer_campo)

    for i in range(1, n):
        for j in range(i, n):
            print("i = ", i, "    j = ", j)
            print("(", matriz[j][i - 1], "-", matriz[j - 1][i - 1], ")/(", vector[j], "-", vector[j - i], ")")
            matriz[j][i] = ((matriz[j][i - 1] - matriz[j - 1][i - 1]) / (vector[j] - vector[j - i]))
            print("matriz[", j, "][", i, "] = ",
                  (matriz[j][i - 1] - matriz[j - 1][i - 1]) / (vector[j] - vector[j - i]))

    contador = 0
    formula = ""

    for i in range(n):
        formula += "(" + str(matriz[i][i])
        for j in range(contador):
            formula += "*" + "(x-(" + str(vector[j]) + "))"
        formula += ")"
        formula += "+" if i < n - 1 else ""

        contador = contador + 1
        print(matriz[i])

    print(formula)

    formula = solve("-y+" + formula, "y")
    print(formula[0])

    aprx = 0
    mul = 1.0
    for i in range(n):
        mul = matriz[i][i]
        for j in range(1, i + 1):
            mul = mul * (punto_a_evaluar - vector[j - 1])
        aprx = aprx + mul

    print("El valor aproximado de f(", punto_a_evaluar, ") es: ", aprx)
    return formula[0], aprx, matriz



def formulaIntro(x, formula):
    solucion = solve("-y+" + formula, "y")
    solucion = eval(str(solucion[0]))

    print(solucion)
    return solucion


def simpson(formula, nodos, a, b):

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

    return  formula, solucion, ""




class GUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Ecuaciones')

        self.grid()

        self.out = tk.StringVar()
        self.out.set("")
        self.lbl = tk.Label(self, text="f(x) = ")

        self.in_str = tk.Entry(self)
        #Valor por defecto
        #self.in_str.insert(tk.END, 'x*e^(-x)-0.2')

        #Menu de metodos
        self.default_choice = tk.StringVar()
        self.default_choice.set('Diferencias Divididas')
        self.menu = tk.OptionMenu(self, self.default_choice, 'Diferencias Divididas', 'Simpson Compuesto')

        self.button = tk.Button(self, text='Resolver', cursor='hand1', command=self.process)

        self.lbl.grid(row=0, sticky='nsew')
        self.in_str.grid(row=0, column=1, sticky='nsew')

        #Valores por defecto del menu row=1
        self.menu.grid(row=3, column=0, sticky='nsew')
        self.button.grid(row=3, column=1, sticky='nsew')

        self.lbl.config(font=("Ubuntu Mono", 30) , bg='white')
        self.in_str.config(font=("Ubuntu Mono", 30), bg='white')
        self.button.config(font=("Ubuntu Mono", 30), bg='white')
        self.menu.config(font=("Ubuntu Mono", 30), bg='white')

        self.labels = {}
        self.s_tbl = ''
        #self.bool_table = False

        # Valores por defecto del epsilon y toletancia row=1
        self.primer_campo = tk.Entry(self)
        self.primer_campo.insert(tk.END, '-2,-1,2,3')
        #Ahora son los rangos
        #self.epsilon.insert(tk.END, 'n/a')


        self.segundo_campo = tk.Entry(self)
        self.segundo_campo.insert(tk.END, '4,1,4,9')

        self.tercer_campo = tk.Entry(self)
        self.tercer_campo.insert(tk.END, "5")
        #ahora son los rangos
        #self.tolerance.insert(tk.END, 'n/a')


        self.primer_campo.grid(row=1, column=0, sticky='nsew')
        self.segundo_campo.grid(row=1, column=1, sticky='nsew')
        self.tercer_campo.grid(row=2, column=0, columnspan=3, sticky='nsew')
        self.primer_campo.config(font=("Ubuntu Mono", 30), bg='white')
        self.segundo_campo.config(font=("Ubuntu Mono", 30), bg='white')
        self.tercer_campo.config(font=("Ubuntu Mono", 30), bg='white')

        self.r = 1

        self.table_shown = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)



    def show_tables(self, event=None):
        #p Configurando las tablas
        print(self.table_shown)
        if self.table_shown == False:
            tab = tk.Text(self)
            tab.grid(row=self.r + 2, columnspan=2)
            vsb = tk.Scrollbar(self, orient='vertical', command=tab.yview)
            tab.configure(yscrollcommand=vsb.set)
            # vsb.grid(row=r+1, column=3)
            tab.insert(tk.END, self.s_tbl)

            self.labels['tab'] = tab
            self.table_shown = True
        else:
            self.labels['tab'].delete(1.0, tk.END)
            self.labels['tab'].destroy()
            self.table_shown = False



    def process(self, event = None):
        self.table_shown = False

        print(self.default_choice.get())

        self.s_tbl = ''

        for (k,v) in self.labels.items():
            if k == 'graph':
                v.get_tk_widget().destroy()
            else:
                v.destroy()

        self.r = 3
        self.grid_rowconfigure(self.r, weight=1)


        #Calculando

        tabla = ""
        if self.default_choice.get() == 'Diferencias Divididas':
            res, aprx, tbl = diferencias(self.primer_campo.get(), self.segundo_campo.get(), self.tercer_campo.get())
            for m in range(len(tbl)):
                tabla += str(tbl[m]) + "\n"

            label = tk.Label(self, text=tabla + '\nFormula' + ': ' + str(res) + "\nResultado: " + str(aprx), anchor="e")

        if self.default_choice.get() == 'Simpson Compuesto':
            res, aprx, tbl = simpson(self.in_str.get(), int(self.tercer_campo.get()), float(self.primer_campo.get()), float(self.segundo_campo.get()))
            label = tk.Label(self, text="Resultado: " + str(aprx), anchor="e")


        # self.s_tbl = mostrar_tabla(tbl,self.s_tbl, self.default_choice.get())





        # print(abs(round(func(res), 2)))
        label.grid(row=4, columnspan=2, sticky='W')
        label.config(font=("Ubuntu Mono", 20))
        self.labels['lbl' + str(self.r - 2)] = label

        self.grid_rowconfigure(self.r, weight=1)

        self.r += 1


        fig = Figure(figsize=(4,4), dpi = 90)
        a = fig.add_subplot(111)

        if self.default_choice.get() == 'Diferencias Divididas':
            a.plot([5], [25], 'ro')
            x = np.arange(0., aprx + 10, 1)
        else:
            x = np.arange(int(self.primer_campo.get()), int(self.segundo_campo.get())+3, step=1)


        f = eval(str(res))

        a.plot(f)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().grid(row=self.r+1, columnspan=2 , sticky = 'nsew')

        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=self.r, columnspan=2)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        self.r += 1
        self.labels['tool'] = toolbar

        self.labels['graph'] = canvas

if __name__ == "__main__":
    MainWindow = GUI()
    MainWindow.bind('<Return>', MainWindow.process)
    MainWindow.mainloop()
