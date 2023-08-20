from src.Controllers.World import World
from src.Settings.Settings import Settings

class Window():
    def __init__(self):
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
    
    def updateObjects(self):
        to_be_Draw = []

        for obj in self.__world.getObjects():
            coordinates = obj.getCoordinates()
            for point in range(len(coordinates)):
                if (not point == (len(coordinates)-1)):
                    p1 = coordinates[point]
                    p2 = coordinates[point + 1]
                    x1, y1, z1 = p1
                    x2, y2, z2 = p2
                    
                else:
                    p1 = coordinates[-1]
                    p2 = coordinates[0]
                    x1, y1, z1 = p1
                    x2, y2, z2 = p2
                
                if(
                    #Point one inside
                    (
                    (((x1 >= self.__Xwmin) and (x1 <= self.__Xwmax)) and
                    ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                    or
                    #Point two inside
                    (((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax)) and
                    ((y2 >= self.__Ywmin) and (y2 <= self.__Ywmax))))

                    or

                    #crossing horizontally
                    (((x1 < self.__Xwmin) and
                    ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                    and
                    ((x2 > self.__Xwmax) and
                    ((y2 >= self.__Ywmin) and (y2 <= self.__Ywmax))))

                    or
                    #crossing vertically
                    (((y1 < self.__Ywmin) and
                    ((x1 >= self.__Xwmin) and (x1 <= self.__Xwmax))) 
                    and
                    ((y2 > self.__Ywmax) and
                    ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))
                    
                    or
                    #crossing diagonally left to top
                    (((x1 < self.__Xwmin) and
                    ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                    and
                    ((y2 < self.__Ywmin) and
                    ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))

                    or
                    #crossing diagonally left to bottom
                    (((x1 < self.__Xwmin) and
                    ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                    and
                    ((y2 > self.__Ywmax) and
                    ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))

                    or
                    #crossing diagonally right to top
                    (((x1 > self.__Xwmax) and
                    ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax))) 
                    and
                    ((y2 < self.__Ywmin) and
                    ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))

                    or
                    #crossing diagonally right to bottom
                    (((x1 > self.__Xwmax) and
                    ((y1 >= self.__Ywmin) and (y1 <= self.__Ywmax)))  
                    and
                    ((y2 > self.__Ywmax) and
                    ((x2 >= self.__Xwmin) and (x2 <= self.__Xwmax))))
                    ):

                    to_be_Draw.append(obj)
                    break
                    
        self.setObjectsToBeDraw(to_be_Draw)
                    
    
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

            transformed_coordinates.append((xw, yw, 0))

        return transformed_coordinates