import tkinter as tk
import app.config

class Sidebar(tk.Frame):
    def __init__(self, master = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.var_matrix_size = tk.StringVar(value="10")

        self.var_xmin = tk.StringVar(value="-2")
        self.var_xmax = tk.StringVar(value="2")
        self.var_ymin = tk.StringVar(value="-2")
        self.var_ymax = tk.StringVar(value="2")

        self.configure(width = app.config.sidebar_width, bg=app.config.sidebar_bg)
        self.pack_propagate(False)
        self.create_widgets()

    def create_widgets(self) -> None:
        self.label = tk.Label(self, text = "Zadejte funkci:")#bere jen promennou z, mocninu jako **, odmocninu **(1/2), funkce napr exp(z)
        self.label.pack(pady=(20,5))


        self.func_input = tk.StringVar()
        self.entry = tk.Entry(self, textvariable = self.func_input)
        self.entry.pack(pady=5, padx=10, fill=tk.X)

        self.button = tk.Button(self, text="Vykreslit", command = self.master.submit)
        self.button.pack(pady=(10,20))


        self.label_matrix = tk.Label(self, text = "Zadejte velikost(rozlišení) matice:")
        self.label_matrix.pack(pady=(20,5))

        self.entry_matrix = tk.Entry(self, textvariable=self.var_matrix_size)
        self.entry_matrix.pack(pady = (10,20))

        
        tk.Label(self, text="Zadejte oblast (xmin, xmax, ymin, ymax):").pack(pady=(10, 0))
        tk.Entry(self, textvariable=self.var_xmin).pack()
        tk.Entry(self, textvariable=self.var_xmax).pack()
        tk.Entry(self, textvariable=self.var_ymin).pack()
        tk.Entry(self, textvariable=self.var_ymax).pack()
        