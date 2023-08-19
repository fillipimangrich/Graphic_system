from src.Controllers.World import World

class Window():
    def __init__(self):
        self.__world = World()
        self.__Xwmin = 0
        self.__Xwmax = 0
        self.__Ywmin = 0
        self.__Ywmax = 0

    def get_world(self):
        return self.__world

    