from src.Controllers.OperationHandler import OperationHandler
from src.Controllers.ViewPort import ViewPort
class Controller():
    def __init__(self):
        self.__operantion_handler = OperationHandler()
        self.__viewport = ViewPort()
        self.__size_of_move = 50


    def getListOfObjects(self):
        return self.__viewport.getWindow().getWorld().getObjects()

    def addObject(self, object):
        self.__viewport.getWindow().getWorld().addObject(object)
    
    def getViewport(self):
        return self.__viewport
    
    def moveUp(self):
        self.__viewport.getWindow().setYwmin(self.__viewport.getWindow().getYwmin() - self.__size_of_move)
        self.__viewport.getWindow().setYwmax(self.__viewport.getWindow().getYwmax() - self.__size_of_move)

    def moveDown(self):
        self.__viewport.getWindow().setYwmin(self.__viewport.getWindow().getYwmin() + self.__size_of_move)
        self.__viewport.getWindow().setYwmax(self.__viewport.getWindow().getYwmax() + self.__size_of_move)
    
    def moveRight(self):  
        self.__viewport.getWindow().setXwmin(self.__viewport.getWindow().getXwmin() + self.__size_of_move)
        self.__viewport.getWindow().setXwmax(self.__viewport.getWindow().getXwmax() + self.__size_of_move)

    def moveLeft(self):
        self.__viewport.getWindow().setXwmin(self.__viewport.getWindow().getXwmin() - self.__size_of_move)
        self.__viewport.getWindow().setXwmax(self.__viewport.getWindow().getXwmax() - self.__size_of_move)

    def zoomIn(self):
        self.__viewport.getWindow().setYwmin(self.__viewport.getWindow().getYwmin() + self.__size_of_move)
        self.__viewport.getWindow().setYwmax(self.__viewport.getWindow().getYwmax() - self.__size_of_move)
        self.__viewport.getWindow().setXwmin(self.__viewport.getWindow().getXwmin() + self.__size_of_move)
        self.__viewport.getWindow().setXwmax(self.__viewport.getWindow().getXwmax() - self.__size_of_move)

    def zoomOut(self):
        self.__viewport.getWindow().setYwmin(self.__viewport.getWindow().getYwmin() - self.__size_of_move)
        self.__viewport.getWindow().setYwmax(self.__viewport.getWindow().getYwmax() + self.__size_of_move)
        self.__viewport.getWindow().setXwmin(self.__viewport.getWindow().getXwmin() - self.__size_of_move)
        self.__viewport.getWindow().setXwmax(self.__viewport.getWindow().getXwmax() + self.__size_of_move)
    