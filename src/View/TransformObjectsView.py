import tkinter as tk
from tkinter import ttk
from src.View.MoveObjectTab import MoveObjectTab
from src.View.ScaleObjectTab import ScaleObjectTab
from src.View.RotateObjectTab import RotateObjectTab
from src.View.TransformationList import TransformationList
from src.View.TransformTabMenu import TransformTabMenu

class TransformObjectsView(tk.Toplevel):
    def __init__(self, master, controller, object):
        super().__init__(master)
        self.controller = controller
        self.title("Transform Object: " + object.getName())
        self.geometry("600x300")
        self.transformation_list = []
        self.tab_menu = TransformTabMenu(self)    
        self.object = object
        
        # Create the object list bar
        self.transf_list = TransformationList(self, controller,  self.transformation_list)
        self.transf_list.grid(row=2, padx=5,pady=5, column=5)
        # define tabs
        self.tabs = [MoveObjectTab(self.tab_menu),
                     ScaleObjectTab(self.tab_menu, controller, object),
                     RotateObjectTab(self.tab_menu, controller, object)]
     
        
        # bind tabs to self.tab_menu
        self.tab_menu.add(self.tabs[0], text='Move')
        self.tab_menu.add(self.tabs[1], text='Scale')
        self.tab_menu.add(self.tabs[2], text='Rotate')
        self.tab_menu.grid(row=2, columnspan=1, pady = 20, padx=10)

        
        apply_button = tk.Button(self, text="Apply Tranformations", font=("Arial", 10), command=self.apply_transformations)
        apply_button.grid(row=6,pady=5, padx=3)
        
    def apply_transformations(self):
        self.controller.apply_transformations(self.transformation_list, self.object)
       
    def add_translation(self, Dx,Dy,Dz, type):
        self.transformation_list.append([Dx, Dy,Dz, type])
        self.transf_list.update_transf_list(self.transformation_list)
        
    def add_scale(self, Sx,Sy, Sz, type):
        self.transformation_list.append([Sx, Sy, Sz, type])
        self.transf_list.update_transf_list(self.transformation_list)
        
    def add_rotation(self, angle, axis, type):
        self.transformation_list.append([angle, axis, type])
        self.transf_list.update_transf_list(self.transformation_list)
        
    def delete_transf(self, index):
        self.transformation_list.pop(index)
        self.transf_list.update_transf_list(self.transformation_list)


