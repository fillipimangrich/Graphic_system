from abc import ABC

class Shape():
    def __init__(self, name, type, x, y) -> None:
        self.__x = x
        self.__y = y
        self.__name = name
        self.__type  = type

    def getX(self):
        return self.__x
    
    def setX(self, x):
        self.__x = x

    def getY(self):
        return self.__y
    
    def setY(self, y):
        self.__y = y
    
    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name
        
    def getType(self):
        return self.__type

    def setType(self, type):
        self.__type = type


