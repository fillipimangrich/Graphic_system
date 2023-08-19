from src.Controllers.OperationHandler import OperationHandler
from src.Controllers.World import World

class Controller():
    def __init__(self):
        self.__operantion_handler = OperationHandler()
        self.__list_of_objects = []
        self.__world = World()


    def getLisOfObjects(self):
        return self.__list_of_objects

    def addObject(self,object):
        self.__list_of_objects.append(object)

    