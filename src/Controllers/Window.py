from src.Controllers.World import World

class Window():
    def __init__(self):
        self.__world = World()
        self.__Xwmin = 0
        self.__Xwmax = 460
        self.__Ywmin = 0
        self.__Ywmax = 920

    def get_world(self):
        return self.__world

    def get_xwmin(self):
        return self.__Xwmin
    
    def get_xwmax(self):
        return self.__Xwmax
    
    def get_Ywmin(self):
        return self.__Ywmin
    
    def get_Ywmax(self):
        return self.__Ywmax

    