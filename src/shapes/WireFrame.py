from Shape import Shape

class WireFrame(Shape):
    def __init__(self) -> None:
        super().__init__()

    def getListOfPoints(self):
        return self.__list_of_points
    
    def setListOfPoints(self, list_of_points):
        self.__list_of_points = list_of_points