from abc import ABC

class Shape():
    def __init__(self, name, type, *coordinates) -> None:
        self.__coordinates = coordinates
        self.__name = name
        self.__type  = type

    #coordinate need to be a tuple (x,y,z)
    def addNewCoordinate(self, coordinate):
        self.__coordinates.append(coordinate)
    
    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name
        
    def getType(self):
        return self.__type

    def setType(self, type):
        self.__type = type


