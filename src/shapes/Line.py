from src.shapes.Shape import Shape
class Line(Shape):
    def __init__(self, name, type, coordinates) -> None:
        super().__init__(name = name, type= type, coordinates=coordinates)
