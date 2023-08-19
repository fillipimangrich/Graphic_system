from src.Controllers.OperationHandler import OperationHandler

class Controller():
    def __init__(self):
        self.__operantion_handler = OperationHandler()


    def getLisOfObjects(self):
        return self.__list_of_objects

    def addObject(self,object):
        self.__list_of_objects.append(object)

    