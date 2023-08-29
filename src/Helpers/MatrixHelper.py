import numpy as np
import math

from src.shapes.Shape import Shape


class MatrixHelper():
    def getRotationMatrix(angle, axis):
        a_cos = math.cos(angle)
        a_sin = math.sin(angle)
        if axis == "x" or axis == (1, 0, 0):
            return np.array(
                [
                    [1, 0, 0, 0],
                    [0, a_cos, a_sin, 0],
                    [0, -a_sin, a_cos, 0],
                    [0, 0, 0, 1],
                ]
            )
        elif axis == "y" or axis == (0, 1, 0):
            return np.array(
                [
                    [a_cos, 0, -a_sin, 0],
                    [0, 1, 0, 0],
                    [a_sin, 0, a_cos, 0],
                    [0, 0, 0, 1],
                ]
            )
        elif axis == "z" or axis == (0, 0, 1):
            return np.array(
                [
                    [a_cos, a_sin, 0, 0],
                    [-a_sin, a_cos, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ]
            )


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
        print('entrou aqui')
        scale_matrix = MatrixHelper.getScaleMatrix(sx, sy, sz)
        center = obj.calcObjectCenter()

        to_origin = MatrixHelper.getTranslationMatrix(-center[0], -center[1], center[2])
        to_position = MatrixHelper.getTranslationMatrix(center[0], center[1], center[2])

        result = np.matmul(to_origin, scale_matrix)
        result = np.matmul(result, to_position)
        return result
    

    def calculateRotationMatrix(obj : Shape, angle, axis):
        center = obj.calcObjectCenter()
        x, y, z, o = center
        to_origin = MatrixHelper.getTranslationMatrix(-x, -y, -z)
        translate_back = MatrixHelper.getTranslationMatrix(x, y, z)

        vector = obj.get_axis_vector(axis)

        beta_on_yz = obj.getBetaOnYz(vector.copy())

        beta_on_xy = obj.getBetaOnXy(vector.copy())

        rotate_to_xy = MatrixHelper.getRotationMatrix(beta_on_yz, "x")
        rotate_from_xy = MatrixHelper.getRotationMatrix(-beta_on_yz, "x")

        rotate_to_y = MatrixHelper.getRotationMatrix(beta_on_xy, "z")
        rotate_from_y = MatrixHelper.getRotationMatrix(-beta_on_xy, "z")

        rotate_on_y = MatrixHelper.getRotationMatrix(angle, "y")

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
    

    def parseTransformationList(obj, transformations):
        matrices = []
        for request in transformations:
            if request[-1] == "translation":
                matrices.append(
                    MatrixHelper.getTranslationMatrix(request[0], request[1], request[2])
                )
            elif request[-1] == "scale":
                matrices.append(
                    MatrixHelper.calculateScaleMatrix(obj, request[0], request[1], request[2])
                )
            else:
                matrices.append(
                    MatrixHelper.calculateRotationMatrix(obj, math.radians(request[0]), request[1])
                )

        return matrices
