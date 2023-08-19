from Shape import Shape

class Line(Shape):
    def __init__(self, x2, y2) -> None:
        super().__init__()
        self.__x2 = x2
        self.__y2 = y2

    def getX2(self):
        return self.__x2
    
    def setX2(self, x2):
        self.__x2 = x2
    
    def getY2(self):
        return self.__y2
    
    def setY2(self, y2):
        self.__y2 = y2