from src.shapes.WireFrame import WireFrame
from src.Helpers.MatrixHelper import MatrixHelper
from src.shapes.Shape import Shape
from src.shapes.Point import Point
from src.shapes.Line import Line
from src.shapes.Curve import Curve
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
        return x,y,0,1
    
    def is_inside_window(self, p, xmin, xmax, ymin, ymax):
        x, y, z, w = p
        return xmin <= x <= xmax and ymin <= y <= ymax

    def get_intersection(self, p1, p2, xmin, xmax, ymin, ymax):
        x0, y0, z0 ,w0 = p1
        x1, y1, z1, w1 = p2

        RC1 = 0
        RC2 = 0

        if (x0 > xmax):
            RC1 += 2
        elif (x0 < xmin):
            RC1 += 1

        if (y0 > ymax):
            RC1 += 8
        elif (y0 < ymin):
            RC1 += 4

        if (x1 > xmax):
            RC2 += 2
        elif (x1 < xmin):
            RC2 += 1

        if (y1 > ymax):
            RC2 += 8
        elif (y1 < ymin):
            RC2 += 4

        if RC1 & RC2:
            return None, None

        m = (y1 - y0) / (x1 - x0) if x1 != x0 else float('inf')

        if RC1 != 0:
            if RC1 & 1:
                y0 = m * (xmin - x0) + y0
                x0 = xmin
            elif RC1 & 2:
                y0 = m * (xmax - x0) + y0
                x0 = xmax
            if RC1 & 4:
                x0 = x0 + (1/m) * (ymin - y0)
                y0 = ymin
            elif RC1 & 8:
                x0 = x0 + (1/m) * (ymax - y0)
                y0 = ymax

        if RC2 != 0:
            if RC2 & 1:
                y1 = m * (xmin - x1) + y1
                x1 = xmin
            elif RC2 & 2:
                y1 = m * (xmax - x1) + y1
                x1 = xmax
            if RC2 & 4:
                x1 = x1 + (1/m) * (ymin - y1)
                y1 = ymin
            elif RC2 & 8:
                x1 = x1 + (1/m) * (ymax - y1)
                y1 = ymax

        return (x0, y0, z0, w0), (x1, y1, z1, w1)

    def label_vertices(self, vertices, xmin, xmax, ymin, ymax):
        labels = []
        for v in vertices:
            if self.is_inside_window(v, xmin, xmax, ymin, ymax):
                labels.append('inside')
            else:
                labels.append('outside')
        return labels
    
    def updateObjects(self, line_clipping_method):

        self.setNormalizedCoordinates()

        to_be_Draw = []

        objs = copy.deepcopy(self.__world.getObjects())
        offset = ((self.__Xwmax-self.__Xwmin)/920)*50
        xmin, ymin = self.__Xwmin+offset, self.__Ywmin+offset
        xmax, ymax = self.__Xwmax-offset, self.__Ywmax-offset
        for obj in objs:

            if type(obj) == Point:
                x,y,z,w = obj.getCoordinates()[0]
                
                if (
                    ((x >= xmin) and (x <= xmax)) and
                    ((y >= ymin) and (y <= ymax))
                    ):
                    to_be_Draw.append(obj)

            elif type(obj) == Line:
                new_coords = None
                if line_clipping_method == 'Cohen–Sutherland':
                    RC1 = 0
                    RC2 = 0
                    x0, y0, z0, w0 = obj.getCoordinates()[0]
                    x1, y1, z1, w1 = obj.getCoordinates()[1]

                    if (x0 > xmax):
                        RC1 += 2
                    elif (x0 < xmin):
                        RC1 += 1
                    
                    if (y0 > ymax):
                        RC1 += 8
                    elif (y0 < ymin):
                        RC1 += 4
                    
                    if (x1 > xmax):
                        RC2 += 2
                    elif (x1 < xmin):
                        RC2 += 1
                    
                    if (y1 > ymax):
                        RC2 += 8
                    elif (y1 < ymin):
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
                            y0_clipped = m * (xmin - x0) + y0
                            x0_clipped = xmin
                        elif RC1 & 2:
                            y0_clipped = m * (xmax - x0) + y0
                            x0_clipped = xmax
                        if RC1 & 4:
                            x0_clipped = x0 + (1/m) * (ymin - y0)
                            y0_clipped = ymin
                        elif RC1 & 8:
                            x0_clipped = x0 + (1/m) * (ymax - y0)
                            y0_clipped = ymax
                        obj.getCoordinates()[0] = (x0_clipped, y0_clipped, z0, w0)
                        

                    if RC2 != 0:
                        if RC2 & 1:
                            y1_clipped = m * (xmin - x1) + y1
                            x1_clipped = xmin+50
                        elif RC2 & 2:
                            y1_clipped = m * (xmax - x1) + y1
                            x1_clipped = xmax
                        if RC2 & 4:
                            x1_clipped = x1 + (1/m) * (ymin - y1)
                            y1_clipped = ymin
                        elif RC2 & 8:
                            x1_clipped = x1 + (1/m) * (ymax - y1)
                            y1_clipped = ymax
                        obj.getCoordinates()[1] = (x1_clipped, y1_clipped, z1, w1)

                    to_be_Draw.append(obj)

                elif line_clipping_method == 'Liang-Barsky':
                    x0, y0, z0, w0 = obj.getCoordinates()[0]
                    x1, y1, z1, w1 = obj.getCoordinates()[1]

                    t0, t1 = 0.0, 1.0
                    dx = x1 - x0
                    dy = y1 - y0

                    p = [-dx, dx, -dy, dy]
                    q = [x0 - (xmin), (xmax) - x0, y0 - (ymin), (ymax) - y0]

                    for i in range(4):
                        if p[i] == 0:
                            if q[i] < 0:
                                break
                        else:
                            t = q[i] / p[i]
                            if p[i] < 0:
                                if t > t1:
                                    break
                                elif t > t0:
                                    t0 = t
                            else:
                                if t < t0:
                                    break
                                elif t < t1:
                                    t1 = t

                    if t0 < t1:
                        x0_clipped = x0 + t0 * dx
                        y0_clipped = y0 + t0 * dy
                        x1_clipped = x0 + t1 * dx
                        y1_clipped = y0 + t1 * dy
                        new_coords = [(x0_clipped, y0_clipped, z0, w0), (x1_clipped, y1_clipped, z1, w1)]

                if new_coords:
                    obj.setCoordinates(new_coords)
                    to_be_Draw.append(obj)

            elif type(obj) == WireFrame:
                #Weiler-Atherton
                vertices = obj.getCoordinates()
                labels = self.label_vertices(vertices, xmin, xmax, ymin, ymax)
                
                new_polygon = []

                for i in range(len(vertices)):
                    start = vertices[i]
                    end = vertices[(i + 1) % len(vertices)]
                    start_label = labels[i]
                    end_label = labels[(i + 1) % len(vertices)]
                    
                    if start_label == 'inside' and end_label == 'inside':
                        new_polygon.append(end.tolist())
                    elif start_label == 'inside' and end_label == 'outside':
                        intersection = self.get_intersection(start, end, xmin, xmax, ymin, ymax)
                        new_polygon.append(list(intersection))
                    elif start_label == 'outside' and end_label == 'inside':
                        intersection = self.get_intersection(start, end, xmin, xmax, ymin, ymax)
                        new_polygon.append(list(intersection))
                        new_polygon.append(end.tolist())

                if new_polygon:
                    flat_polygon = []
                    for point in new_polygon:
                        if isinstance(point, (list, tuple)) and isinstance(point[0], (list, tuple)):
                            flat_polygon.extend(point)
                        else:
                            flat_polygon.append(point)
                    new_obj = WireFrame(obj.getName(), flat_polygon, obj.fill_mode)
                    to_be_Draw.append(new_obj)
                
            elif(type(obj) == Curve):
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
        x,y,z, w = self.getCenter()
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
