from fractions import Fraction
from typing import Self, List, Tuple
from pathlib import PurePath
from xml.dom import minidom as md
class frac:
    """
        frac()
        Things:
        * frac + frac
        * frac - frac
        * frac * frac
        * frac / frac
        * len(frac)
        * frac == frac
        * int
    """
    def __init__(self, Frac1: tuple):
        """
            ### Make a new Fraction Class

            <hr>

            # frac()
            Things:
            * frac + frac
            * frac - frac
            * frac * frac
            * frac / frac
            * len(frac)
            * frac == frac
            * int(frac)
            * frac
        """
        self.numerator = Frac1[0]
        self.denominator = Frac1[1]
        self.frac = Fraction(self.numerator, self.denominator)
    def __mul__(self, other : Self):
        return self.frac * other.frac
    def __add__(self, other : Self):
        return self.frac + other.frac
    def __truediv__(self, other : Self):
        return self.frac / other.frac
    def __sub__(self, other : Self):
        return self.frac - other.frac
    def __eq__(self, other : Self):
        if self.frac == other.frac:
            return True
        elif self.denominator == other.numerator and self.numerator == other.denominator:
            return True
        else:
            return False
    def __int__(self):
        return self.denominator + self.numerator
def load_xml(file: PurePath) -> List[Tuple[int, int]]:
    """
        Load a xml file that has \\<frac\\>\\</frac\\> tags with \\<numerator\\>\\</numerator\\> and \\<dominator\\>\\</dominator\\> tags<hr>
        Returns a list of fraction tuples
    """
    dom = md.parse(file)

    fracs = dom.getElementsByTagName('frac')
    fracl = []
    for frac in fracs:
        numerator = int(frac.getElementsByTagName('numerator')[0].childNodes[0].nodeValue)
        dominator = int(frac.getElementsByTagName('dominator')[0].childNodes[0].nodeValue)
        fracl.append((numerator, dominator))
    return fracl
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

if len(sys.argv) == 1:
    print("Please give the --xmlfile or -xf flag with the file path or the --gui or -g flag")
elif sys.argv[1] == "--xmlfile" or sys.argv[1] == "-xf":
    file = sys.argv[3]
    equ = load_xml(os.path.join(os.getcwd(), file))
    fracl = []
    for i in equ:
        fracl.append(frac(i))
    tfracl = []
    for i in fracl:
        tfracl.append(i.frac)

    def returny():
        if cmb2.get() == '+':messagebox.showinfo('Project Fractionallity', f'Result: {Fraction(cmb1.get()) + Fraction(cmb3.get())}')
        if cmb2.get() == '-':messagebox.showinfo('Project Fractionallity', f'Result: {Fraction(cmb1.get()) - Fraction(cmb3.get())}')
        if cmb2.get() == '*':messagebox.showinfo('Project Fractionallity', f'Result: {Fraction(cmb1.get()) * Fraction(cmb3.get())}')
        if cmb2.get() == '/':messagebox.showinfo('Project Fractionallity', f'Result: {Fraction(cmb1.get()) / Fraction(cmb3.get())}')
    
    win = tk.Tk()

    cmb1 = ttk.Combobox(win, values=tfracl)
    cmb1.grid(column=0, row=0, padx=20, pady=20)

    cmb2 = ttk.Combobox(win, values=['+', '-', '*', '/'])
    cmb2.grid(column=1, row=0, padx=20, pady=20)

    cmb3 = ttk.Combobox(win, values=tfracl)
    cmb3.grid(column=2, row=0, padx=20, pady=20)

    btn = tk.Button(win, text="Show result", command=returny)
    btn.grid(column=1, row=1, padx=20, pady=20)

    win.mainloop()
elif sys.argv[1] == "-g" or sys.argv[1] == "--gui":

    def btnyf():
        f1 = Fraction(f'{f1n.get()}/{f1d.get()}')
        f2 = Fraction(f'{f2n.get()}/{f2d.get()}')
        if operator.get() == '+':messagebox.showinfo('Project Fractionallity', f'Result: {f1 + f2}')
        if operator.get() == '-':messagebox.showinfo('Project Fractionallity', f'Result: {f1 - f2}')
        if operator.get() == '*':messagebox.showinfo('Project Fractionallity', f'Result: {f1 * f2}')
        if operator.get() == '/':messagebox.showinfo('Project Fractionallity', f'Result: {f1 / f2}')
        

    win = tk.Tk()

    f1n = ttk.Spinbox(win, from_=1, to=10000000, state="readonly")
    f1l = tk.Label(win, text="———————")
    f1d = ttk.Spinbox(win, from_=1, to=10000000, state="readonly")

    f1n.grid(column=0, row=0, padx=20, pady=20)
    f1l.grid(column=0, row=1, padx=20, pady=20)
    f1d.grid(column=0, row=2, padx=20, pady=20)

    operator = ttk.Combobox(win, values=["+",'-','*','/'], state="readonly")

    operator.grid(column=1, row=1, padx=20, pady=20)

    f2n = ttk.Spinbox(win, from_=1, to=10000000, state="readonly")
    f2l = tk.Label(win, text="———————")
    f2d = ttk.Spinbox(win, from_=1, to=10000000, state="readonly")

    f2n.grid(column=2, row=0, padx=20, pady=20)
    f2l.grid(column=2, row=1, padx=20, pady=20)
    f2d.grid(column=2, row=2, padx=20, pady=20)

    btny = tk.Button(win, text="Do Operation", command=btnyf)
    btny.grid(column=1, row=3, padx=20, pady=20)

    win.mainloop()