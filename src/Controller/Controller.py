

class Controller():
    def __init__(self):
        self.__list_of_objects = []

    def getLisOfObjects(self):
        return self.__list_of_objects

    def addObject(self,object):
        self.__list_of_objects.append(object)

    