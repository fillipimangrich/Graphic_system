from src.Helpers.MatrixHelper import MatrixHelper
from src.shapes.Shape import Shape
from src.Controllers.World import World
from src.Settings.Settings import Settings
import numpy as np

WINDOW_COORDINATES = [
    (0, 0, 0, 1),
    (0, 460, 0, 1),
    (920, 460, 0, 1),
    (920, 0, 0, 1),
]

class Window(Shape):
    def __init__(self):
        super().__init__(name="window", coordinates=WINDOW_COORDINATES)
        self.__world = World()
        self.__objects_to_be_draw = []
        self.__size = [920, 460]
        self.__Xwmin = 0
        self.__Xwmax = 920
        self.__Ywmin = 0
        self.__Ywmax = 460
        self.__angle = 0
        self.__axis = 'x'
    
    def getObjectsToBeDraw(self):
        return self.__objects_to_be_draw

    def setObjectsToBeDraw(self, objects_to_be_draw):
        self.__objects_to_be_draw = objects_to_be_draw

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
    
    def updateObjects(self):
        to_be_Draw = []

        for obj in self.__world.getObjects():
            if (self.__angle != 0):
                matrix = MatrixHelper.calculateRotationMatrix(obj, np.radians(self.__angle), self.__axis)
                obj.transform(matrix)

            to_be_Draw.append(obj)
                    
        self.setObjectsToBeDraw(to_be_Draw)
                    
    
    def windowTransform(self, coordinates):
        transformed_coordinates = []

        for tuple in coordinates:
            x_v = tuple[0]
            y_v = tuple[1]
            z_v = tuple[2]
            w_v = tuple[3]

            Xwmin = self.getXwmin()
            Xwmax = self.getXwmax()

            Ywmin = self.getYwmin()
            Ywmax = self.getYwmax()
            
            multx = Settings.XVPMAX - Settings.XVPMIN
            multy = Settings.YVPMAX - Settings.YVPMIN

            xw = Xwmin + (x_v - Settings.XVPMIN) / multx * (Xwmax - Xwmin)
            yw = Ywmin + (1 - (y_v - Settings.XVPMIN) / multy) * (Ywmax - Ywmin)

            transformed_coordinates.append((xw, yw, z_v, w_v))

        return transformed_coordinates

    def rotate(self, angle, axis):
        self.__angle = angle
        self.__axis = axis