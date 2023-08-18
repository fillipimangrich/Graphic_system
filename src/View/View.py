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
        self.setControlView()
        self.setAddObjectButton()
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

    def setControlView(self) -> None:
        self.__control = tk.Canvas(
            self.__window,bg = "#565656",height = 420,width = 300,bd = 0,highlightthickness = 0,relief = "ridge")
        self.__control.place(x=20, y=280)
        self.setAddObjectButton()

    def setAddObjectButton(self) -> None:
        self.__add_object_button = tk.PhotoImage(file = f"src/Images/add_button.png")
        button_add = self.__control.create_image(220, 50, image=self.__add_object_button)
        # self.__control.tag_bind(button_add, "<Button-1>", lambda x: )
