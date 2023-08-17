import tkinter as tk

class View():
    def __init__(self) -> None:
        self.__window = tk.Tk()

    def run(self):
        self.__window.mainloop()

app = View()
app.run()