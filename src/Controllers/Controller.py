from src.Controllers.OperationHandler import OperationHandler
from src.Controllers.ViewPort import ViewPort
class Controller():
    def __init__(self):
        self.__operantion_handler = OperationHandler()
        self.__list_of_objects = []
        self.__viewport = ViewPort()


    def getLisOfObjects(self):
        return self.__list_of_objects

    def addObject(self, object):
        self.__list_of_objects.append(object)

    