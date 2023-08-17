import tkinter as tk

class View():
    def __init__(self) -> None:
        self.__window = tk.Tk()

    def run(self) -> None:
        self.__window.geometry("1280x720")
        self.__window.configure(bg = "#2D2D2D")
        self.setViewPort()
        self.setLogOfActionsView()
        self.setListOfObjectsView()
        self.__window.mainloop()

    def setViewPort(self) -> None:
        self.__view_port = tk.Canvas(
            self.__window,bg = "#FFFFFF",height = 460,width = 920,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__view_port.place(x=340, y=20)

    def setLogOfActionsView(self) -> None:
        self.__log_actions_view = tk.Canvas(
            self.__window,bg = "#FFFFFF",height = 200,width = 920,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__log_actions_view.place(x=340, y=500)
    
    def setListOfObjectsView(self) -> None:
        self.__list_of_objects_view = tk.Canvas(
            self.__window,bg = "#FFFFFF",height = 240,width = 300,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__list_of_objects_view.place(x=20, y=20)





app = View()
app.run()