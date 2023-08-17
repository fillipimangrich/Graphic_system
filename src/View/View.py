import tkinter as tk

class View():
    def __init__(self) -> None:
        self.__window = tk.Tk()

    def run(self):
        self.setCanvas()
        self.__window.geometry("1280x720")
        self.__window.configure(bg = "#000000")
        self.__window.mainloop()

    def setCanvas(self) -> None:
        self.__canvas = tk.Canvas(
            self.__window,bg = "#000000",height = 720,width = 1280,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

app = View()
app.run()