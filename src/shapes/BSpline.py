from src.shapes.Shape import Shape

class BSpline(Shape):
    def __init__(self, name, coordinates) -> None:
        super().__init__(name=name, coordinates=coordinates)