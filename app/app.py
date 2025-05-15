import tkinter as tk
from tkinter import messagebox

from app.sidebar import Sidebar
from app.mainframe import MainFrame
from app.newton import create_complex_matrix, NewtonMethod
from app.input_parser import InputParser



class App(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Newtonovy fraktály")
        self.geometry("1000x600+100+100")
        self.minsize(400, 300)

        self.create_widgets()
        self.place_widgets()
        
    def create_widgets(self) -> None:
        self.sidebar = Sidebar(self)
        self.mainframe = MainFrame(self)

    def place_widgets(self) -> None:
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.mainframe.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    def get_input_parser(self,parser):
        self.parser = parser
        print("funkce prijata do App")

    def submit(self):
        #spousti prevedeni funkce, vypocet newtonem a vykresleni fraktalu
        try: 
            #bere vstupy pro funkci, rozměry a rozliseni matice ze sidebaru
            function_str = self.sidebar.func_input.get()
            matrix_size_str = self.sidebar.var_matrix_size.get()
            xmin = float(self.sidebar.var_xmin.get())
            xmax = float(self.sidebar.var_xmax.get())
            ymin = float(self.sidebar.var_ymin.get())
            ymax = float(self.sidebar.var_ymax.get())

            #kontrola, že velikost matice odpovida nejakemu rozumnemu rozmeru
            matrix_size = int(matrix_size_str)
            if matrix_size < 10 or matrix_size > 800:
                raise ValueError("rozměr musí být mezi 10 a 800!")
            
            if xmin >= xmax or ymin >= ymax:
                raise ValueError("neplatný rozsah: xmin musí být menší než xmax a ymin menší než ymax.")

            
            #vola parser pro prevod funkce
            parser = InputParser(function_str)
            print(f"funkce: {parser.func_sym}")
            print("funkce úspěšně převedena:)")
            print(f"hodnota pro z=(1+1j): {parser.evaluate_f(1+1j)}, derivace: {parser.derive_f(1+1j)}")#kontrola pro z = (1+1j)

            #pocita se pocet korenu nejdrive pro male rozliseni matice
            low_grid = create_complex_matrix(100, xmin, xmax, ymin, ymax)
            low_solver = NewtonMethod(parser.f, parser.df, low_grid)
            low_solver.run()
            known_roots = low_solver.roots

            #newtonova metoda se spousti pro velikost matice zadanou uzivatelem, pracuje ale s jiz nalezenymi koreny z predchoziho vypoctu
            grid = create_complex_matrix(matrix_size, xmin, xmax, ymin, ymax)
            newton = NewtonMethod(parser.f, parser.df, grid,known_roots=known_roots)
            root_indices, iterations, _ = newton.run()

            #volani vykresleni fraktalu
            self.mainframe.plot_fractal(root_indices, iterations)
            print(f"počet kořenů:{len(newton.roots)}")


        except ValueError as e:
            messagebox.showerror("Neplatná funkce",str(e))
