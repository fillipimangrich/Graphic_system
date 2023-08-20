import copy
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

    def update(self):
        self.__window.updateObjects()
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

            transformed_coordinates.append((xvp, yvp, 0))

        return transformed_coordinates
