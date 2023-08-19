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

            Xwmin = self.__window.get_xwmin()
            Xwmax = self.__window.get_xwmax()

            Ywmin = self.__window.get_Ywmin()
            Ywmax = self.__window.get_Ywmax()

            xvp = ((xw - Xwmin) / (Xwmax - Xwmin)) * (self.__Xvpmax - self.__Xvpmin)
            yvp = self.__Yvpmin + ((yw - Ywmin) / (Ywmax - Ywmin)) * (self.__Yvpmax - self.__Yvpmin)

            transformed_coordinates.append((xvp, yvp))

        return transformed_coordinates
