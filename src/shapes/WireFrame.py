from src.shapes.Shape import Shape

class WireFrame(Shape):
    def __init__(self, name , coordinates, fill_mode) -> None:
        super().__init__(name=name, coordinates=coordinates)
        self.fill_mode = fill_mode
