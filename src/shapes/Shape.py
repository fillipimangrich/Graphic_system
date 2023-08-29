from abc import ABC
import random
import numpy as np

class Shape():
    def __init__(self, name, coordinates, color='#000000') -> None:
        self.__id = random.randint(1, 1000000)
        self.__name = name
        self.__coordinates = coordinates
        self.toHomogeneousCoordinates()
        self.__color = color
        self.__axis = self.createAxis()

    def createAxis(self):
        axis = np.asarray([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
        center = self.calcObjectCenter()

        if len(center) < 4:
            center = np.append(center, 0)

        new = []
        for element in axis:
            element = np.add(element, center)
            new.append(element)

        return np.asarray(new)
    
    def updateAxis(self, transformation_matrix):
        new = []
        for vector in self.__axis:
            new_v = np.matmul(vector, transformation_matrix)
            new.append(new_v)
        self.__axis = new

    #coordinate need to be a tuple (x,y,z)
    def addNewCoordinate(self, coordinate):
        self.__coordinates.append(coordinate)

    def setCoordinates(self, coordinates):
        self.__coordinates = coordinates
        self.toHomogeneousCoordinates()
    
    def getId(self):
        return self.__id
    
    def setId(self, id):
        self.__id = id

    def getCoordinates(self):
        return self.__coordinates
    
    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name
        
    def getType(self):
        return self.__type

    def setType(self, type):
        self.__type = type
    
    def getColor(self):
        return self.__color
    
    def setColor(self, color):
        self.__color = color
    
    def calcObjectCenter(self):
        points = self.getCoordinates()
        center = np.mean(points, axis=0)
        return center
    
    def toHomogeneousCoordinates(self):
        new_coordinates = []
        for coordinate in self.__coordinates:
            new_c = np.array(coordinate)
            if len(coordinate) < 4:
                new_c = np.append(new_c, 1)
            new_coordinates.append(new_c)

        coordinates = np.array(new_coordinates)
        self.__coordinates = coordinates
    
    def checkNullity(self, vector):
        v = vector.copy()
        v = v**2
        v = np.round(v, decimals=10)
        r = np.sum(v)
        if r == 0:
            return True
        return False

    def getBetaOnXy(self, vector):
        vector = vector[:3]
        vector[2] = 0
        if self.checkNullity(vector):
            return 0.0
        beta = np.arccos(np.clip(np.dot(vector, [0, 1, 0]), -1.0, 1.0))

        if vector[0] < 0:
            beta *= -1

        return beta
    
    def getBetaOnYz(self, vector):
        vector = vector[:3]
        vector[0] = 0
        if self.checkNullity(vector):
            return 0.0
        
        beta = np.arccos(np.clip(np.dot(vector, [0, 1, 0]), -1.0, 1.0))

        if vector[2] < 0:
            beta *= -1

        return beta
    
    # returns the x, y and z axis of the object based on obj center
    def get_axis_vector(self, axis):
        center = self.calcObjectCenter()
        if axis == "x":
            vector = self.__axis[0].copy() - center
        elif axis == "y":
            vector = self.__axis[1].copy() - center
        elif axis == "z":
            vector = self.__axis[2].copy() - center
        else:
            vector = np.asarray(axis) - center
            vector = np.append(vector, 0)

        vector = vector / np.linalg.norm(vector)
        return vector
    
    def transform(self, transformation_matrix):
        new_coordinates = []
        for point in self.__coordinates:
            new_tuple = np.matmul(point, transformation_matrix)
            new_tuple = new_tuple / new_tuple[3]
            new_coordinates.append(new_tuple)
        self.setCoordinates(new_coordinates)
        self.updateAxis(transformation_matrix)