from tkinter.simpledialog import Dialog
from tkinter import Radiobutton, StringVar, Label


class ChoiceDialog(Dialog):
    def body(self, master):
        self.var = StringVar()
        self.var.set("Arame")

        Label(master, text="Escolha uma opção:").pack(anchor="w")

        options = ["Arame", "Grelha", "Preenchido"]
        for option in options:
            Radiobutton(master, text=option, variable=self.var, value=option).pack(anchor="w")

        return None

    def apply(self):
        self.result = self.var.get()