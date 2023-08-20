from abc import ABC

class Shape():
    def __init__(self, name, coordinates, color='#000000') -> None:
        self.__name = name
        self.__coordinates = coordinates
        self.__color = color

    #coordinate need to be a tuple (x,y,z)
    def addNewCoordinate(self, coordinate):
        self.__coordinates.append(coordinate)

    def setCoordinates(self, coordinates):
        self.__coordinates = coordinates

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