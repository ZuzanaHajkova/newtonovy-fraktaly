import numpy as np
from app.config import tol, max_it
from sklearn.cluster import DBSCAN

def create_complex_matrix(matrix_size, xmin, xmax, ymin, ymax):
        
  real = np.linspace(xmin, xmax, matrix_size)
  imag = np.linspace(ymin, ymax, matrix_size)

  return (real[np.newaxis,:] + 1j * imag[:,np.newaxis]).astype(np.complex64)

  #vytvori se matice komplexni roviny

class NewtonMethod:
  def __init__(self, f, df, grid, known_roots = None):

    self.f = f
    self.df = df
    self.grid = grid
    self.tol = tol
    self.max_it = max_it

    self.shape = grid.shape
    #seznam nalezených kořenů, pro prvni vypocet s malou matici prazdna mnozina, pro druhy vypocet seznam predesle nalezenych korenu
    self.roots = known_roots if known_roots is not None else [] 
    self.root_indices = np.full(grid.shape, -1, dtype=np.int16) #matice, kde je ke kazdemu bodu prirazeny index korene ke kteremu smeruje
    self.iterations = np.zeros(grid.shape, dtype=np.uint8) #matice kde je kazdemu bodu prirazeny pocet iteraci nez konvergoval
    self.final_values = np.zeros(grid.shape, dtype=np.complex64)#matice kde je kazdemu bodu prirazena hodnota korene ke kteremu konverguje

  def newtons_method(self,z0):
    #vypocita newtonovu metodu pro jeden bod, vrati konecny bod a pocet iteraci
    z = z0

    for n in range(self.max_it):
      try:
        if not np.isfinite(self.f(z)) or not np.isfinite(self.df(z)) or self.df(z)==0:
          return np.nan, self.max_it
        #hlida uz vstupy funkce a derivace

        z_new = z - (self.f(z) / self.df(z))
        #pocita nove z(newtonova metoda)

        if not np.isfinite(z_new):
         return np.nan, self.max_it
         #hlida divergentni body

        if abs(z_new - z) < self.tol:
          return z_new, n
        z = z_new
    
      except (ZeroDivisionError,FloatingPointError,ValueError, OverflowError):
        return np.nan, self.max_it
        #hlida divergentni body
    
    return z, self.max_it
  
  def match_root(self, z):
    #prirazuje index korenum
    for i, r in enumerate(self.roots):
      if abs(z - r) < self.tol * 10:
        return i
    return -1

  def compute(self):
  #vola newtonovu metodu pro kazdy bod z komplexi mrizky a uklada vysledky jako matice
    for r in range(self.shape[0]):
      for j in range(self.shape[1]):
        z0 = self.grid[r,j]
        z, n_iter = self.newtons_method(z0)
        if np.isfinite(z):
          self.final_values[r, j]= np.round(z,decimals = 4)
          self.iterations[r, j] = n_iter
          if self.roots:
           self.root_indices[r, j] = self.match_root(z)#pokud jsou nalezene koreny, priradi se jim indexy
        else:
          self.final_values[r, j] = np.nan
          self.iterations[r, j] = self.max_it
          self.root_indices[r, j] = -1
          #pokud jsou nalezene koreny divergentni, oznaci se indexem jako nenalezene



  def find_roots(self):
    flat_values = self.final_values.flatten()#prevod na 2D matici
    nan_mask = np.isfinite(flat_values)#hlida NaN koreny

    points = np.vstack([flat_values.real[nan_mask], flat_values.imag[nan_mask]]).T

    #spusteni clusteringu - slouci hodnoty blizko sebe do jedne a da jim label (-1 pro šum)
    db = DBSCAN(eps=self.tol * 10, min_samples=3).fit(points)
    labels = db.labels_

    #odstraneni divergujicich bodu 
    valid_mask = labels != -1
    labels = labels[valid_mask]
    points = points[valid_mask]

    #unikatni labely(pro kazdy koren)
    unique_labels = np.unique(labels)
    self.roots = []

    #pro kazdy label urcuje prumernou hodnotu korenu
    for label in unique_labels:
      cluster_points = points[labels == label]
      avg_root = cluster_points.mean(axis=0)
      self.roots.append(avg_root[0] + 1j * avg_root[1])

    #zacne se s matici obsahujici vsude -1(nenalezene koreny), ty se pak nahradi jen tam, kde byly nalezeny platne koreny
    root_indices = -1 * np.ones_like(flat_values, dtype=int)
    nan_maskret = np.where(nan_mask)[0]
    root_indices[nan_maskret[valid_mask]] = labels
    self.root_indices = root_indices.reshape(self.shape)
  
  def run(self):
    #spousti cely vypocet a vraci matice s koreny, iteracemi a pocet korenu 
    self.compute()
    #hledani korenu se spousti jen pro vypocet s malou velikosti matice, aby probehl v akceptovatelnem case
    if not self.roots:
      self.find_roots()

    return self.root_indices, self.iterations, len(self.roots)


         




                  
             


    


