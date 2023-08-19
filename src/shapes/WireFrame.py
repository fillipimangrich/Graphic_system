from Shape import Shape

class WireFrame(Shape):
    def __init__(self, list_of_points) -> None:
        super().__init__()
        self.__list_of_points = list_of_points

    def getListOfPoints(self):
        return self.__list_of_points
    
    def setListOfPoints(self, list_of_points):
        self.__list_of_points = list_of_points