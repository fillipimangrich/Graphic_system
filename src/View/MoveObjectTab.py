import tkinter as tk

class MoveObjectTab(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.object = object

        # Instantiate elements
        container = tk.LabelFrame(self, text='Amount')
        self.entry_x = tk.Entry(container, width=5)
        self.entry_y = tk.Entry(container, width=5)
        self.entry_z = tk.Entry(container, width=5)
        label_x = tk.Label(container, text='x:')
        label_y = tk.Label(container, text='y:')
        label_z = tk.Label(container, text='z:')
        apply_button = tk.Button(self, text="Add", font=("Arial", 10), command=self.add_translation)

        container.grid(pady=15, padx=10, row=0)        
        apply_button.grid(row=0, column=1, sticky="SE",pady=15, padx=10)
        label_x.grid(row=0, column=0, padx=5, pady=5)
        self.entry_x.grid(row=0, column=1, padx=5, pady=5)

        label_y.grid(row=0, column=2, padx=5, pady=5)
        self.entry_y.grid(row=0, column=3, padx=5, pady=5)

        label_z.grid(row=0, column=4, padx=5, pady=5)
        self.entry_z.grid(row=0, column=5, padx=5, pady=5)    
        
    def add_translation(self):
        Dx = float(self.entry_x.get())
        Dy = float(self.entry_y.get())
        Dz = float(self.entry_z.get())
        type = "translation"
        self.master.add_translation(Dx, Dy, Dz, type)