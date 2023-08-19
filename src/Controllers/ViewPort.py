from src.Controllers.Window import Window

class ViewPort():
    def __init__(self):
        self.__window = Window()
        self.__Xvpmin = 0
        self.__Xvpmax = 0
        self.__Yvpmin = 0
        self.__Yvpmax = 0
    
    def getWindow(self):
        return self.__window
    
    def viewportTransform(self, coordinates):
        transformed_coordinates = []

        delta_x_w, delta_y_w = 2, 2
        x_w_min, y_w_min = -1, -1

        delta_x_vp, delta_y_vp = self.getDeltas()

        for tuple in coordinates:
            xw = tuple[0]
            yw = tuple[1]
            xvp = ((xw - x_w_min) / delta_x_w) * (delta_x_vp)
            yvp = (1 - ((yw - y_w_min) / delta_y_w)) * (delta_y_vp)
            transformed_coordinates.append((xvp, yvp))
        return transformed_coordinates
    
    def getDeltas(self):
        d_x = self.__Xvpmax - self.__Xvpmin
        d_y = self.__Yvpmax - self.__Yvpmin

        return d_x, d_y

    