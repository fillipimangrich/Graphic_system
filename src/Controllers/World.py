
class World():
    def __init__(self):
        self.__list_of_objects = []

    def addObject(self, object):
        self.__list_of_objects.append(object)
        print(object.getCoordinates())

    def getObjects(self):
        return self.__list_of_objects
    
    def removeObject(self, object):
        for obj in self.__list_of_objects:
            if obj.getId() == object.getId():
                self.__list_of_objects.remove(obj)

    def getObjectById(self, id):
        for obj in self.__list_of_objects:
            if obj.getId() == id:
                return obj
    