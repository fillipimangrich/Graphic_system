from src.Controller.OperationHandler import OperationHandler

class Controller():
    def __init__(self):
        self.__operantion_handler = OperationHandler()
        self.__list_of_objects = []

    def getLisOfObjects(self):
        return self.__list_of_objects

    def addObject(self,object):
        self.__list_of_objects.append(object)

    