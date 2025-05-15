import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import cm
import app.config


class MainFrame(tk.Frame):
   def __init__(self, master = None, *args, **kwargs):
      super().__init__(master, *args,**kwargs)

      self.configure(bg="white")

      self.figure = Figure(app.config.figsize, app.config.dpi)
      self.ax = self.figure.add_subplot(111)
      self.ax.axis('on')

      self.canvas = FigureCanvasTkAgg(self.figure, master=self)
      self.canvas_widget = self.canvas.get_tk_widget()
      self.canvas_widget.pack(fill=tk.BOTH, expand=True)
      #figure se bude zobrazovat v canvas okna
     
   def plot_fractal(self, root_indices, iterations):
      #vykresli fraktal
      self.ax.clear()

      #prevedeni hodnot do rozmezi 0-1 pro pouziti s tab10
      iterations_mod = (iterations/iterations.max())
      roots_mod = (root_indices/root_indices.max())

      #barevne rozliseni korenu
      color_map = cm.tab10(roots_mod)
      #sytosti rozlisena rychlost konvergence
      color_map[...,-1] = iterations_mod**0.5

      self.ax.imshow(color_map, origin='lower')
      self.ax.axis('off')
      self.canvas.draw()

      print("Max iterací:", iterations.max())
  

      

     
     