from src.shapes.Shape import Shape

class OBJ(Shape):
    def __init__(self, name , coordinates, fill_mode, faces) -> None:
        super().__init__(name=name, coordinates=coordinates)
        self.fill_mode = fill_mode
        self.faces = faces
