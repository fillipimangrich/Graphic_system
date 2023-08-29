
import tkinter as tk

class TransformationList(tk.LabelFrame):
    def __init__(self, master, controller, transformation_list):
        super().__init__(
            master,
            width=200,
            height=400,
            bg="lightgray",
            text = "Transformation List"
        )

        self.controller = controller

        listvariable = tk.StringVar()
        self.listbox = tk.Listbox(self, listvariable=listvariable, cursor="hand1", selectmode=tk.SINGLE)
        self.listbox.pack(pady=5, side=tk.TOP, fill=tk.X)

        delete_object_button = tk.Button(self, text="Delete", font=("Arial", 10), command=self.delete_transf)
        delete_object_button.pack(pady=5, side=tk.LEFT,padx=3)

    def update_transf_list(self, transf_list):
        self.listbox.delete(0,tk.END) 
        for obj in transf_list:
            self.listbox.insert(tk.END,obj[-1])
            
    def delete_transf(self):
        if(self.listbox.curselection()):
            number = self.listbox.curselection()[0]
            self.master.delete_transf(number)
        else:
            self.controller.show_warning("No object selected!")