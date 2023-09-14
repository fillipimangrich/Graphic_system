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
            # coordinates = obj.getCoordinates()
            # for point in range(len(coordinates)):
                # if (not point == (len(coordinates)-1)):
                #     p1 = coordinates[point]
                #     p2 = coordinates[point + 1]
                #     x1, y1, z1, w = p1
                #     x2, y2, z2, w = p2
                    
                # else:
                #     p1 = coordinates[-1]
                #     p2 = coordinates[0]
                #     x1, y1, z1, w = p1
                #     x2, y2, z2, w = p2
                
                # if(
                #     #Point one inside
                #     (
                #     (((x1 >= self.__Xwmin) and (x1 <= self.__Xwmax)) and
                #     ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                #     or
                #     #Point two inside
                #     (((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax)) and
                #     ((y2 >= self.__Ywmin) and (y2 <= self.__Ywmax))))

                #     or

                #     #crossing horizontally
                #     (((x1 < self.__Xwmin) and
                #     ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                #     and
                #     ((x2 > self.__Xwmax) and
                #     ((y2 >= self.__Ywmin) and (y2 <= self.__Ywmax))))

                #     or
                #     #crossing vertically
                #     (((y1 < self.__Ywmin) and
                #     ((x1 >= self.__Xwmin) and (x1 <= self.__Xwmax))) 
                #     and
                #     ((y2 > self.__Ywmax) and
                #     ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))
                    
                #     or
                #     #crossing diagonally left to top
                #     (((x1 < self.__Xwmin) and
                #     ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                #     and
                #     ((y2 < self.__Ywmin) and
                #     ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))

                #     or
                #     #crossing diagonally left to bottom
                #     (((x1 < self.__Xwmin) and
                #     ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                #     and
                #     ((y2 > self.__Ywmax) and
                #     ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))

                #     or
                #     #crossing diagonally right to top
                #     (((x1 > self.__Xwmax) and
                #     ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                #     and
                #     ((y2 < self.__Ywmin) and
                #     ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))

                #     or
                #     #crossing diagonally right to bottom
                #     (((x1 > self.__Xwmax) and
                #     ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax)))  
                #     and
                #     ((y2 > self.__Ywmax) and
                #     ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))
                #     ):

                #     to_be_Draw.append(obj)
                #     break
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
        angle = np.radians(angle)
        matrix = MatrixHelper.calculateRotationMatrix(self, angle, axis)
        self.transform(matrix)