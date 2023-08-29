import numpy as np
import math


class MatrixHelper():

    #DELETE AFTER
    def generate_translation_matrix(origin_point, destination_point):
        diff = [destination_point[i]-origin_point[i] for i in range(3)]
        diff.append(1)

        matrix = np.array([
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            diff])
        
        return np.dot(origin_point, matrix)
    
    #DELETE AFTER
    def generate_scaling_matrix(origin_point, x_scale, y_scale, z_scale):
        point = np.array(origin_point)

        matrix = np.array([[x_scale, 0, 0, 0],
            [0, y_scale, 0, 0],
            [0, 0, z_scale, 0],
            [0, 0, 0, 1]])

        return np.dot(point, matrix)
    
    #DELETE AFTER   
    def generate_rotation_matrix(origin_point, angle):
        point = np.array(origin_point)

        radians_angle = math.radians(angle)

        matrix = np.array([[math.cos(radians_angle),-math.sin(radians_angle),0],
                    [math.sin(radians_angle), math.cos(radians_angle),0],
                    [0,0,1]])
        
        print(matrix)

        return np.dot(point, matrix)
    

    def getScaleMatrix(sx, sy, sz):
        scale_matrix = np.array(
            [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]]
        )
        return scale_matrix


    def calculateTransformationMatrix(transformations):
        transformation_matrix = np.eye(4)

        for matrix in transformations:
            transformation_matrix = np.matmul(transformation_matrix, matrix)
        return transformation_matrix
    

    def getTranslationMatrix(dx, dy, dz):
        translation_matrix = np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [dx, dy, dz, 1]]
        )
        return translation_matrix
    

    def calculateScaleMatrix(obj, sx, sy, sz):
        scale_matrix = MatrixHelper.getScaleMatrix(sx, sy, sz)
        center = obj.calcObjectCenter()

        to_origin = MatrixHelper.getTranslationMatrix(-center[0], -center[1], center[2])
        to_position = MatrixHelper.getTranslationMatrix(center[0], center[1], center[2])

        result = np.matmul(to_origin, scale_matrix)
        result = np.matmul(result, to_position)
        return result
    

    def calculateRotationMatrix(obj, angle, axis):
        center = obj.calcObjectCenter()
        x, y, z, o = center
        to_origin = MatrixHelper.getTranslationMatrix(-x, -y, -z)
        translate_back = MatrixHelper.getTranslationMatrix(x, y, z)

        vector = obj.get_axis_vector(axis)

        beta_on_yz = obj.get_beta_on_yz(vector.copy())

        beta_on_xy = obj.get_beta_on_xy(vector.copy())

        rotate_to_xy = obj.get_rotation_matrix(beta_on_yz, "x")
        rotate_from_xy = obj.get_rotation_matrix(-beta_on_yz, "x")

        rotate_to_y = obj.get_rotation_matrix(beta_on_xy, "z")
        rotate_from_y = obj.get_rotation_matrix(-beta_on_xy, "z")

        rotate_on_y = obj.get_rotation_matrix(angle, "y")

        matrices = [
            to_origin,
            rotate_to_xy,
            rotate_to_y,
            rotate_on_y,
            rotate_from_y,
            rotate_from_xy,
            translate_back,
        ]
        result = np.eye(4)

        for n in range(7):
            result = np.matmul(result, matrices[n])

        return result
    

    def parseTransformationList(transformations):
        matrices = []
        for request in transformations:
            if request[-1] == "translation":
                matrices.append(
                    MatrixHelper.getTranslationMatrix(request[0], request[1], request[2])
                )
            elif request[-1] == "scale":
                matrices.append(
                    MatrixHelper.calculateScaleMatrix(request[0], request[1], request[2])
                )
            else:
                matrices.append(
                    MatrixHelper.calculateRotationMatrix(math.radians(request[0]), request[1])
                )

        return matrices
