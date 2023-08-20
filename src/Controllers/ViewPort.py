from src.Controllers.Window import Window

class ViewPort():
    def __init__(self):
        self.__window = Window()
        self.__Xvpmin = 0
        self.__Xvpmax = 460
        self.__Yvpmin = 0
        self.__Yvpmax = 920
    
    def getWindow(self):
        return self.__window
    
    def viewportTransform(self, coordinates):
        transformed_coordinates = []

        for tuple in coordinates:
            xw = tuple[0]
            yw = tuple[1]

            Xwmin = self.__window.getXwmin()
            Xwmax = self.__window.getXwmax()

            Ywmin = self.__window.getYwmin()
            Ywmax = self.__window.getYwmax()

            sx = (self.__Xvpmax - self.__Xvpmin) / (Xwmax - Xwmin)
            sy = (self.__Yvpmax - self.__Yvpmin) / (Ywmax - Ywmin)
        
            xvp = self.__Xvpmin + ((xw - Xwmin) * sx)
            yvp = self.__Yvpmin + ((yw - Ywmin) * sy)

            transformed_coordinates.append((xvp, yvp))

        return transformed_coordinates
