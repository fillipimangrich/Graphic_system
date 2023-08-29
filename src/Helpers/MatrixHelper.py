import numpy as np
import math


class MatrixHelper():

    def generate_translation_matrix(origin_point, destination_point):
        diff = [destination_point[i]-origin_point[i] for i in range(3)]
        diff.append(1)

        matrix = np.array([
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            diff])
        
        return np.dot(origin_point, matrix)
    
    
    def generate_scaling_matrix(origin_point, x_scale, y_scale, z_scale):
        point = np.array(origin_point)

        matrix = np.array([[x_scale, 0, 0, 0],
            [0, y_scale, 0, 0],
            [0, 0, z_scale, 0],
            [0, 0, 0, 1]])

        return np.dot(point, matrix)
    

    def generate_rotation_matrix(origin_point, angle):
        point = np.array(origin_point)

        radians_angle = math.radians(angle)

        matrix = np.array([[math.cos(radians_angle),-math.sin(radians_angle),0],
                    [math.sin(radians_angle), math.cos(radians_angle),0],
                    [0,0,1]])
        
        print(matrix)

        return np.dot(point, matrix)
