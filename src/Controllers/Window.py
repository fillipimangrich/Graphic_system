from src.Helpers.MatrixHelper import MatrixHelper
from src.shapes.Shape import Shape
from src.Controllers.World import World
from src.Settings.Settings import Settings
import copy

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
        self.__Xwmin = 0
        self.__Xwmax = 920
        self.__Ywmin = 0
        self.__Ywmax = 460

    
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

    def getCenter(self):
        x = ((self.getXwmax()-self.getXwmin())/2)+self.getXwmin()
        y = ((self.getYwmax()-self.getYwmin())/2)+self.getYwmin()
        return x,y,0
    
    def updateObjects(self):
        to_be_Draw = []

        for obj in self.__world.getObjects():
           # cliping here
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

    def setNormalizedCoordinates(self):
        normalized_coordinates = []

        for obj in self.__world.getObjects():
            obj_copy = copy.deepcopy(obj)
            new_coordinates = []
            for x,y,z,w in obj_copy.getCoordinates():
                new_x = ((x/(self.getXwmax()-self.getXwmin()))-0.5)*2
                new_y = ((y/(self.getYwmax()-self.getYwmin()))-0.5)*2
                new_coordinates.append((new_x,new_y,z,w))

            normalized_coordinates.append(obj_copy)
                    
        self.__normalized_coordinates = normalized_coordinates


    def rotate(self, angle, axis):
        x,y,z = self.getCenter()
        for obj in self.__world.getObjects():
            transform_matrix = MatrixHelper.calculateWindowRotationMatrix(obj,angle,axis,x,y,z)
            obj.transform(transform_matrix)