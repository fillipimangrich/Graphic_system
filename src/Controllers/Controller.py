from src.Controllers.OperationHandler import OperationHandler
from src.Controllers.ViewPort import ViewPort
class Controller():
    def __init__(self):
        self.__operantion_handler = OperationHandler()
        self.__viewport = ViewPort()


    def getListOfObjects(self):
        return self.__viewport.getWindow().get_world().getObjects()

    def addObject(self, object):
        self.__viewport.getWindow().get_world().addObject(object)
    
    def getViewport(self):
        return self.__viewport

    