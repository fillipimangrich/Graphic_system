import tkinter as tk
from tkinter import ttk

class TransformTabMenu(ttk.Notebook):
    def __init__(self, master):
        super().__init__(
            master,
            width=380
            )

    def add_translation(self, Dx, Dy, Dz, type):
        self.master.add_translation(Dx,Dy,Dz, type)

    def add_scale(self, Sx, Sy, Sz, type):
        self.master.add_scale(Sx,Sy,Sz, type)

    def add_rotation(self, angle, axis, type):
        self.master.add_rotation(angle,axis, type)