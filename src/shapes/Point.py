from src.Shapes.Shape import Shape

class Point(Shape):
    def __init__(self, name, coordinates) -> None:
        super().__init__(name=name, coordinates=coordinates)