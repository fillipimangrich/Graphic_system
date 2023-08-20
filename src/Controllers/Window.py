from src.Controllers.World import World
from src.Settings.Settings import Settings

class Window():
    def __init__(self):
        self.__world = World()
        self.__Xwmin = 0
        self.__Xwmax = 460
        self.__Ywmin = 0
        self.__Ywmax = 920

    def getWorld(self):
        return self.__world

    def getXwmin(self):
        return self.__Xwmin
    
    def setXwmin(self, Xwmin):
        self.__Xwmin = Xwmin
    
    def getXwmax(self):
        return self.__Xwmax
    
    def setXwmax(self, Xwmax):
        self.__Xwmax = Xwmax
    
    def getYwmin(self):
        return self.__Ywmin
    
    def setYwmin(self, Ywmin):
        self.__Ywmin = Ywmin
    
    def getYwmax(self):
        return self.__Ywmax
    
    def setYwmax(self, Ywmax):
        self.__Ywmax = Ywmax
    
    def windowTransform(self, coordinates):

        transformed_coordinates = []

        for tuple in coordinates:
            x_v = tuple[0]
            y_v = tuple[1]

            Xwmin = self.getXwmin()
            Xwmax = self.getXwmax()

            Ywmin = self.getYwmin()
            Ywmax = self.getYwmax()

            sx = (Settings.XVPMAX - Settings.XVPMIN) / (Xwmax - Xwmin)
            sy = (Settings.YVPMAX - Settings.XVPMIN) / (Ywmax - Ywmin)

            xw = (x_v - Settings.XVPMIN) / sx + Xwmin
            yw = (y_v - Settings.YVPMIN) / sy + Ywmin

            transformed_coordinates.append((xw, yw))

        return transformed_coordinates