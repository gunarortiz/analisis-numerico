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

from scipy.misc import derivative

def mostrar_tabla(table, out, algo='Newton Raphson'):
    if out != '':
        out += '\n'

    if algo == 'Biseccion':
        for (i, row) in enumerate(table):
            #print('[' + str(i + 1) + ']', row)
            out += '[' + str(i + 1) + ']'.join(row)+'\n'
    else:
        for row in table:
            out += str(row) + '\n'

    return out

def prepocess_input(inp):
    in_str = ''
    res_str = ''
    inp = inp.replace(' ','')
    decomp = inp.split('e')
    print(decomp)

    for v in decomp:
        if v == '':
            continue
        elif v[0] == 'x' and v[1] == 'p':
            print('entre1')
            res_str = res_str + 'e' + v
        else:
            if v[0] == '^':
                print('entre2')
                res_str = res_str + 'exp' + v[1:]
            else:
                print('entre3')
                res_str += v
        print('res_str:', res_str)
    for ch in res_str:
        if ch == '^':
            in_str += '**'
        else:
            in_str += ch

    print('final value:',in_str)
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
    intersect = []
    projections = []
    a = solve_math_errors(f, a, eps)

    prev = f((a-1)+eps)
    for x_i in range(a,b+1):

        act = f(x_i+eps)

        if act*prev <= 0 + eps:
            #print((prev, act, act*prev))
            intersect.append((x_i - 1 + eps, x_i + eps))
            #projections.append((f(x_i - 1 + eps), f(x_i + eps)))
        prev = act

    xs = np.linspace(-6.5,6.5, 100)
    ys = []
    for x_i in xs:
        ys.append(f(x_i))
    return intersect, xs, ys, projections




#no se utiliza

def biseccion(a, b, its, f, tol):
    a_orig, b_orig = a,b
    sw = False

    im_X_m = a_orig
    m_prev = nan
    #k = 0
    while sw == False:
        #k += 1
        print('a, b:',a,b)
        #a,b = int(a),int(b)
        table = []
        for it in range(its):

            X_m = (a + b) / 2.0

            res = X_m

            if res == m_prev:
                break

            im_a, im_b, im_X_m = f(a), f(b), f(X_m)

            table.append([str(a) + (' ^+' if im_a > 0 else ' ^-'),
                         str(b) + (' ^+' if im_b > 0 else ' ^-'),
                         str(X_m) + (' ^+' if im_X_m > 0 else ' ^-')])

            if im_X_m > 0:
                b = X_m
            else:
                a = X_m

            m_prev = X_m

        if sw == True:
            break

        if abs(round(f(res),2)) <= tol:
        #if abs(round(f(res), 2)) <= 0.05:
            sw = True
        else:
            b = a_orig
            a = b_orig

    #print(k)
    return res, (True if (f(res) == 0) else False), table

def newton_raphson(a, b, its, f, tol):
    res = a

    sw = False

    while sw == False:
        table = []
        x = Symbol('x')
        for it in range(its):
            res = res - (f(res) / derivative(f, res, dx=1e-10))
            #res = res - f.evalf(subs={x:res}) / diff(f,x).evalf(subs={x:res})
            # res = res - ( f(res) / dx(res) )
            table.append(res)

        if sw == True:
            break

        #0.05
        if abs(round(f(res),2)) <= tol:
        #if abs(round(f.evalf(subs={x:res}))) <= tol:
            sw = True
        else:
            res = b

    return res, (True if (f(res) == 0) else False), table
    #return res, (True if (f.evalf(subs={x:res}) == 0) else False), table

def secante(a, b, its, f, eps, tol):
    x_i0 = a
    x_i1 = b

    sw = False

    while sw == False:
        table = []
        for it in range(its):
            temp = (x_i0 * f(x_i1) - x_i1 * f(x_i0)) / (f(x_i1) - f(x_i0) + eps)
            table.append(temp)
            x_i0 = x_i1
            x_i1 = temp

        if sw == True:
            break

        if abs(round(f(x_i1),2)) <= tol:
            sw = True
        else:
            x_i0 = b
            x_i1 = a

    return x_i1, (True if (f(x_i1) == 0) else False), table

# hasta aqui no se usa

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
        self.default_choice.set('Biseccion')
        self.menu = tk.OptionMenu(self, self.default_choice, 'Biseccion', 'Newton Raphson', 'Secante')

        self.button = tk.Button(self, text='Resolver', cursor='hand1', command=self.process)

        self.lbl.grid(row=0, sticky='nsew')
        self.in_str.grid(row=0, column=1, sticky='nsew')

        #Valores por defecto del menu row=1
        self.menu.grid(row=2, column=0, sticky='nsew')
        self.button.grid(row=2, column=1, sticky='nsew')

        self.lbl.config(font=("Ubuntu Mono", 30) , bg='white')
        self.in_str.config(font=("Ubuntu Mono", 30), bg='white')
        self.button.config(font=("Ubuntu Mono", 30), bg='white')
        self.menu.config(font=("Ubuntu Mono", 30), bg='white')

        self.labels = {}
        self.s_tbl = ''
        #self.bool_table = False

        # Valores por defecto del epsilon y toletancia row=1
        self.epsilon = tk.Entry(self)
        self.epsilon.insert(tk.END, '1e-15')
        #Ahora son los rangos
        #self.epsilon.insert(tk.END, 'n/a')


        self.tolerance = tk.Entry(self)
        self.tolerance.insert(tk.END, '0.05')
        #ahora son los rangos
        #self.tolerance.insert(tk.END, 'n/a')


        self.epsilon.grid(row=1, column=0, sticky='nsew')
        self.tolerance.grid(row=1, column=1, sticky='nsew')
        self.epsilon.config(font=("Ubuntu Mono", 30), bg='white')
        self.tolerance.config(font=("Ubuntu Mono", 30), bg='white')

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
        eps = 1e-15
        #eps = 1e-8
        tol = 0.05

        #eps = float(self.epsilon.get())
        #tol = float(self.tolerance.get())
        iters = 100
        for (k,v) in self.labels.items():
            if k == 'graph':
                v.get_tk_widget().destroy()
            else:
                v.destroy()

        func = prepocess_input(self.in_str.get().lower())

        transformations = (standard_transformations + (implicit_multiplication_application,))

        X = Symbol('x')
        parsed = parse_expr(func, transformations=transformations)
        func = lambdify((X), parsed)

        intersect, xs, ys, projections = intersecciones(func, -50, 50, eps)
        self.out.set(intersect)

        # row number (starting in 2 because of inputs)
        #self.r = 2
        self.r = 3
        self.grid_rowconfigure(self.r, weight=1)

        #if(self.epsilon.get() != 'n/a' && self.tolerance.get() != 'n/a'):
        #    a =

        print(intersect)
        print(projections)
        if len(intersect) == 0:
            label = tk.Label(self, text='No se encontraron soluciones')
            label.grid(row=self.r, columnspan=2, sticky='nsew')
            label.config(font=("Ubuntu Mono", 30), bg='white')
            self.labels['lbl0'] = label
            self.r += 1

        px,py = [],[]

        #Calculando
        prev = None
        for e in intersect:
            if self.default_choice.get() == 'Biseccion':
                res, sw, tbl = biseccion(e[0], e[1], iters, func, tol)
            if self.default_choice.get() == 'Newton Raphson':
                #res, sw, tbl = newton_raphson(e[0], e[1], iters, parsed, tol)
                res, sw, tbl = newton_raphson(e[0], e[1], iters, func, tol)
            if self.default_choice.get() == 'Secante':
                res, sw, tbl = secante(e[0], e[1], iters, func, 1e-16, tol)

            if prev is not None:
                prev = round(prev,5)
            #print('=', prev, round(res,5))
            if abs(func(res)) > 0.0005 or prev == round(res,5):
                continue

            prev = res
            self.s_tbl = mostrar_tabla(tbl,self.s_tbl, self.default_choice.get())
            #print(res, '->', abs(round(func(res), 2)))
            px.append(res)
            py.append(0)

            label = tk.Label(self, text='x'+str(self.r-2)+': '+str(res))
            print(abs(round(func(res), 2)))
            label.grid(row=self.r, columnspan=2, sticky='W')
            label.config(font=("Ubuntu Mono", 30))
            self.labels['lbl' + str(self.r - 2)] = label

            self.grid_rowconfigure(self.r, weight=1)

            self.r += 1

        fig = Figure(figsize=(5,4), dpi = 120)
        a = fig.add_subplot(111)
        a.plot(xs,ys)
        a.plot(px,py, 'ro')
        a.axhline(y=0, linewidth=0.5, color='k')
        a.axvline(x=0, linewidth=0.5,color='k')
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().grid(row=self.r+1, columnspan=2 , sticky = 'nsew')

        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=self.r, columnspan=2)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        self.r += 1
        self.labels['tool'] = toolbar

        self.labels['graph'] = canvas

        m_tbl = tk.Button(self, text='Mostrar Tabla', cursor='hand1', command=self.show_tables)
        m_tbl.grid(row=self.r+1, columnspan=2, sticky='nsew')
        m_tbl.config(font=("Ubuntu Mono", 30), bg='white')

        self.labels['most_tbl'] = m_tbl
        self.grid_rowconfigure(self.r+1, weight=1)

if __name__ == "__main__":
    MainWindow = GUI()
    MainWindow.bind('<Return>', MainWindow.process)
    MainWindow.mainloop()
