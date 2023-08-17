from abc import ABC

class Shape():
    def __init__(self, name, type) -> None:
        self.__name = name
        self.__type  = type

    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name
        
    def getType(self):
        return self.__type

    def setType(self, type):
        self.__type = type


