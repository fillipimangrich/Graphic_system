from src.Controllers.Window import Window

class ViewPort():
    def __init__(self):
        self.__window = Window()
        self.__Xvpmin = 0
        self.__Xvpmax = 0
        self.__Yvpmin = 0
        self.__Yvpmax = 0
    
    def get_window(self):
        return self.__window

    