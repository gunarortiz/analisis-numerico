import tkinter as tk

class GUI(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.default_choice = tk.StringVar()
        self.default_choice.set('Biseccion')
        self.menu = tk.OptionMenu(self, self.default_choice, 'Biseccion', 'Newton Raphson', 'Secante')
        self.menu.option_get()
        self.menu.grid()

        self.button = tk.Button(self, text='Resolver', cursor='hand1', command=self.process)

        self.button.grid()

    def process(self, event=None):
        print(self.default_choice.get())

if __name__ == '__main__':
    MainWindow = GUI()
    MainWindow.mainloop()


