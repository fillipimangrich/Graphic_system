from src.shapes.Shape import Shape
from src.Controllers.OperationHandler import OperationHandler
from src.Controllers.ViewPort import ViewPort
from src.Settings.Settings import Settings
from src.Helpers.MatrixHelper import MatrixHelper


class Controller():
    def __init__(self):
        self.__operantion_handler = OperationHandler()
        self.__viewport = ViewPort()
        self.__size_of_move = 50
        self.__scale = 0.1
        self.chosen_clipping_algorithm = "Cohen–Sutherland"
        

    def getListOfObjects(self): 
        return self.__viewport.getObjectsToBeDrawTransformed()

    def getListOfObjectsOfWorld(self):
        return self.__viewport.getWindow().getWorld().getObjects()
    
    def addObject(self, object : Shape):
        object.setCoordinates(self.__viewport.getWindow().windowTransform(object.getCoordinates())) 
        self.__viewport.getWindow().getWorld().addObject(object)
        self.__viewport.update(self.chosen_clipping_algorithm)

    def removeObject(self, object):
        self.__viewport.getWindow().getWorld().removeObject(object)
        self.__viewport.update(self.chosen_clipping_algorithm)
    
    def popWorldObject(self):
        self.__viewport.getWindow().getWorld().getObjects().pop()
        self.update()
    
    def getViewport(self):
        return self.__viewport
    
    def update(self):
        self.__viewport.update(self.chosen_clipping_algorithm)

    def setColorById(self, id, color):
        obj = self.__viewport.getWindow().getWorld().getObjectById(id)
        obj.setColor(color)
    
    def moveUp(self):
        self.__viewport.getWindow().setYwmin(self.__viewport.getWindow().getYwmin() - (self.__size_of_move))
        self.__viewport.getWindow().setYwmax(self.__viewport.getWindow().getYwmax() - (self.__size_of_move))
        self.__viewport.update(self.chosen_clipping_algorithm)

    def moveDown(self):
        self.__viewport.getWindow().setYwmin(self.__viewport.getWindow().getYwmin() + (self.__size_of_move))
        self.__viewport.getWindow().setYwmax(self.__viewport.getWindow().getYwmax() + (self.__size_of_move))
        self.__viewport.update(self.chosen_clipping_algorithm)
    
    def moveRight(self):  
        self.__viewport.getWindow().setXwmin(self.__viewport.getWindow().getXwmin() + (self.__size_of_move))
        self.__viewport.getWindow().setXwmax(self.__viewport.getWindow().getXwmax() + (self.__size_of_move))
        self.__viewport.update(self.chosen_clipping_algorithm)

    def moveLeft(self):
        self.__viewport.getWindow().setXwmin(self.__viewport.getWindow().getXwmin() - (self.__size_of_move))
        self.__viewport.getWindow().setXwmax(self.__viewport.getWindow().getXwmax() - (self.__size_of_move))
        self.__viewport.update(self.chosen_clipping_algorithm)

    def zoomIn(self):
        self.__viewport.getWindow().setYwmin(self.__viewport.getWindow().getYwmin() + (self.__scale * Settings.HEIGHT))
        self.__viewport.getWindow().setYwmax(self.__viewport.getWindow().getYwmax() - (self.__scale * Settings.HEIGHT))
        self.__viewport.getWindow().setXwmin(self.__viewport.getWindow().getXwmin() + (self.__scale * Settings.WIDTH))
        self.__viewport.getWindow().setXwmax(self.__viewport.getWindow().getXwmax() - (self.__scale * Settings.WIDTH))
        self.__viewport.update(self.chosen_clipping_algorithm)

    def zoomOut(self):
        self.__viewport.getWindow().setYwmin(self.__viewport.getWindow().getYwmin() - (self.__scale * Settings.HEIGHT))
        self.__viewport.getWindow().setYwmax(self.__viewport.getWindow().getYwmax() + (self.__scale * Settings.HEIGHT))
        self.__viewport.getWindow().setXwmin(self.__viewport.getWindow().getXwmin() - (self.__scale * Settings.WIDTH))
        self.__viewport.getWindow().setXwmax(self.__viewport.getWindow().getXwmax() + (self.__scale * Settings.WIDTH))
        self.__viewport.update(self.chosen_clipping_algorithm)

    def applyTransformations(self, transf_list, objectId):
        obj = self.__viewport.getWindow().getWorld().getObjectById(objectId)
        matrices = MatrixHelper.parseTransformationList(obj, transf_list)
        transf_matrix = MatrixHelper.calculateTransformationMatrix(matrices)
        obj.transform(transf_matrix)
        self.__viewport.update(self.chosen_clipping_algorithm)
    
    def rotateWindow(self, angle, axis):
        self.__viewport.getWindow().rotate(angle, axis)
        self.__viewport.update(self.chosen_clipping_algorithm)
    