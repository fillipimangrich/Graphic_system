from src.Helpers.MatrixHelper import MatrixHelper
from src.shapes.Shape import Shape
from src.shapes.Point import Point
from src.shapes.Line import Line
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
    
    def getNormalizedCoordenates(self):
        return self.__normalized_coordinates

    def getCenter(self):
        x = ((self.getXwmax()-self.getXwmin())/2)+self.getXwmin()
        y = ((self.getYwmax()-self.getYwmin())/2)+self.getYwmin()
        return x,y,0
    
    def updateObjects(self, line_clipping_method):

        self.setNormalizedCoordinates()

        to_be_Draw = []

        objs = copy.deepcopy(self.__world.getObjects())
        
        for obj in objs:
            if type(obj) == Point:
                x,y,z,w = obj.getCoordinates()[0]
                
                if (
                    ((x >= self.__Xwmin+50) and (x <= self.__Xwmax-50)) and
                    ((y >= self.__Ywmin+50) and (y <= self.__Ywmax-50))
                    ):
                    to_be_Draw.append(obj)

            elif type(obj) == Line:
                RC1 = 0
                RC2 = 0
                x0, y0, z0, w0 = obj.getCoordinates()[0]
                x1, y1, z1, w1 = obj.getCoordinates()[1]

                if (x0 > self.__Xwmax-50):
                    RC1 += 2
                elif (x0 < self.__Xwmin+50):
                    RC1 += 1
                
                if (y0 > self.__Ywmax-50):
                    RC1 += 8
                elif (y0 < self.__Ywmin+50):
                    RC1 += 4
                
                if (x1 > self.__Xwmax-50):
                    RC2 += 2
                elif (x1 < self.__Xwmin+50):
                    RC2 += 1
                
                if (y1 > self.__Ywmax-50):
                    RC2 += 8
                elif (y1 < self.__Ywmin+50):
                    RC2 += 4

                if ((RC1 == 0) and (RC2 == 0)):
                    to_be_Draw.append(obj)
                    continue

                if RC1 & RC2:
                    continue 

                x0_clipped, y0_clipped = x0, y0
                x1_clipped, y1_clipped = x1, y1

                m = (y1 - y0) / (x1 - x0) if x1 != x0 else None 

                if RC1 != 0:
                    if RC1 & 1:
                        y0_clipped = m * (self.__Xwmin+50 - x0) + y0
                        x0_clipped = self.__Xwmin+50
                    elif RC1 & 2:
                        y0_clipped = m * (self.__Xwmax-50 - x0) + y0
                        x0_clipped = self.__Xwmax -50
                    if RC1 & 4:
                        x0_clipped = x0 + (1/m) * (self.__Ywmin+50 - y0)
                        y0_clipped = self.__Ywmin+50
                    elif RC1 & 8:
                        x0_clipped = x0 + (1/m) * (self.__Ywmax-50 - y0)
                        y0_clipped = self.__Ywmax-50
                    obj.getCoordinates()[0] = (x0_clipped, y0_clipped, z0, w0)
                    

                if RC2 != 0:
                    if RC2 & 1:
                        y1_clipped = m * (self.__Xwmin+50 - x1) + y1
                        x1_clipped = self.__Xwmin+50
                    elif RC2 & 2:
                        y1_clipped = m * (self.__Xwmax-50 - x1) + y1
                        x1_clipped = self.__Xwmax-50
                    if RC2 & 4:
                        x1_clipped = x1 + (1/m) * (self.__Ywmin+50 - y1)
                        y1_clipped = self.__Ywmin+50
                    elif RC2 & 8:
                        x1_clipped = x1 + (1/m) * (self.__Ywmax-50 - y1)
                        y1_clipped = self.__Ywmax-50
                    obj.getCoordinates()[1] = (x1_clipped, y1_clipped, z1, w1)

                to_be_Draw.append(obj)

                
                        
                    
            else:
                for coordinate in obj.getCoordinates():
                    x,y,z,w = coordinate
                    if (
                        ((x >= self.__Xwmin) and (x <= self.__Xwmax)) and
                        ((y >= self.__Ywmin) and (y <= self.__Ywmax))
                        ):
                        to_be_Draw.append(obj)
                        break
                    

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


                # #calculate the intersect point if one of the points is in the left of the window and the other is inside the window
                # if ((RC1 == 1) and (RC2 == 0)):
                #     m = (y1-y0)/(x1-x0)
                #     y_intersect = m*(self.__Xwmin-x0)+y0
                #     if (y_intersect > self.__Ywmin and y_intersect < self.__Ywmax):
                #         obj.getCoordinates()[0] = (self.__Xwmin, y_intersect,0,1)
                #         to_be_Draw.append(obj)
                #     continue
                
                # if ((RC1 == 1) and (RC2 == 8)):
                #     m = (y1-y0)/(x1-x0)
                #     y_intersect = m*(self.__Xwmin-x0)+y0
                #     x_intersect = x0+((1/m)*(self.__Ywmax-y0))
                #     if (y_intersect > self.__Ywmin and y_intersect < self.__Ywmax):
                #         obj.getCoordinates()[0] = (self.__Xwmin, y_intersect,0,1)
                #         obj.getCoordinates()[1] = (x_intersect, self.__Ywmax,0,1)
                #         to_be_Draw.append(obj)
                #     continue
                        
                # if ((RC1 == 1) and (RC2 == 4)):
                #     m = (y1-y0)/(x1-x0)
                #     y_intersect = m*(self.__Xwmin-x0)+y0
                #     x_intersect = x0+((1/m)*(self.__Ywmin-y0))
                #     if (y_intersect > self.__Ywmin and y_intersect < self.__Ywmax):
                #         print(y0, y_intersect)
                #         obj.getCoordinates()[0] = (self.__Xwmin, y_intersect,0,1)
                #         obj.getCoordinates()[1] = (x_intersect, self.__Ywmin,0,1)
                #         to_be_Draw.append(obj)
                #     continue
