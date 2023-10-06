


class DescritorOBJ():

    def __init__(self):
        pass

    def parseOBJ(self, file_path):
        file = open(file_path, "r")
        lines = file.readlines()
        name = ""
        vertices = []
        for line in lines:
            if line[0] == "g":
                name = line.split()[1]
            elif(line[0] in ["v", "vt", "vn", "vp"]):
                _,x,y,z = line.split()
                vertices.append((float(x),float(y),0))
            elif(line[0] == "a"):
                break
        return name, vertices


