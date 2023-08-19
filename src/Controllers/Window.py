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
    
    def setXwmin(self, Xwmin):
        self.__Xwmin = Xwmin
    
    def get_xwmax(self):
        return self.__Xwmax
    
    def setXwmax(self, Xwmax):
        self.__Xwmax = Xwmax
    
    def get_Ywmin(self):
        return self.__Ywmin
    
    def setYwmin(self, Ywmin):
        self.__Ywmin = Ywmin
    
    def get_Ywmax(self):
        return self.__Ywmax
    
    def setYwmax(self, Ywmin):
        self.__Ywmin = Ywmin

    