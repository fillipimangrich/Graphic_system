import copy
from src.Settings.Settings import Settings
from src.Controllers.Window import Window

class ViewPort():
    def __init__(self):
        self.__window = Window()
        self.__objects_to_be_draw_transformed = []
        self.__Xvpmin = 0
        self.__Xvpmax = 920
        self.__Yvpmin = 0
        self.__Yvpmax = 460
    
    def getWindow(self):
        return self.__window
    
    def setObjectsToBeDrawTransformed(self, objects_to_be_draw_transformed):
        self.__objects_to_be_draw_transformed = objects_to_be_draw_transformed
    
    def getObjectsToBeDrawTransformed(self):
        return self.__objects_to_be_draw_transformed

    def update(self, line_clipping_method):
        self.__window.updateObjects(line_clipping_method)
        self.transformAllObjects()

    def transformAllObjects(self):
        to_be_draw_copy = copy.deepcopy(self.__window.getObjectsToBeDraw())
        for obj in to_be_draw_copy:
            new_coordinates = self.viewportTransform(obj.getCoordinates())
            obj.setCoordinates(new_coordinates)
        
        self.__objects_to_be_draw_transformed = to_be_draw_copy

    

    def viewportTransform(self, coordinates):
        transformed_coordinates = []

        for tuple in coordinates:
            x_v = tuple[0]
            y_v = tuple[1]
            z_v = tuple[2]
            w_v = tuple[3]

            Xwmin = self.__window.getXwmin()
            Xwmax = self.__window.getXwmax()

            Ywmin = self.__window.getYwmin()
            Ywmax = self.__window.getYwmax()

            xvp = (x_v - Xwmin) / (Xwmax - Xwmin)
            xvp *= (Settings.XVPMAX - Settings.XVPMIN)

            yvp = 1 - (y_v - Ywmin) / (Ywmax - Ywmin)
            yvp *= (Settings.YVPMAX - Settings.YVPMIN)

            transformed_coordinates.append((round(xvp), round(yvp), z_v, w_v))

        return transformed_coordinates
