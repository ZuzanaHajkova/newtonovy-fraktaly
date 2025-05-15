import sympy as sp
from sympy import symbols, diff
from sympy.parsing.sympy_parser import parse_expr

class InputParser:
    def __init__(self, function_str: str):
        self.function_str = function_str
        self.symbol = symbols('z')

        self.func_sym = None
        self.der_sym = None

        self.f = None
        self.df = None

        self.parse_function()
    def parse_function(self)->None:
        try:
            self.func_sym = parse_expr(self.function_str)#prevadi funkci na symbolickou
            self.der_sym = diff(self.func_sym,self.symbol)#symbolicka derivace

            if self.der_sym == 0:
                raise ValueError("derivace je nulová, zadejte funkci s proměnnou 'z'")


            self.f = sp.lambdify(self.symbol, self.func_sym,modules = 'numpy')#volatelna funkce pro vypocty
            self.df = sp.lambdify(self.symbol, self.der_sym, modules = 'numpy')#volatelna zderivovana funkce

            if not self.func_sym.free_symbols <= {self.symbol}:#hlida ze ve funkci nejsou jine promenne nez z
                print(f"Chyba: {e}")
                raise ValueError("Neplatná funkce, zadejte funkci s proměnnou 'z'")

        except Exception as e:
            print(f"Chyba: {e}")
            raise ValueError("Neplatná funkce")
            # zastavi neplatne symboly

    def evaluate_f(self,z):
        return self.f(z) 
        #vraci funkcni hodnotu v bode z
    
    def derive_f(self,z):
        return self.df(z)
        #vraci hodnotu derivace v z
        

        