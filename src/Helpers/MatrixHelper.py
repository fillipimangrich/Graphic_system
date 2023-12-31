import numpy as np
import math
from functools import reduce

from src.shapes.Shape import Shape


class MatrixHelper():

    def getRotationMatrixByAngleAndAxis(angle, axis):
        if axis == "x" or axis == (1, 0, 0):
            return np.array(
                [
                    [1, 0, 0, 0],
                    [0, math.cos(angle), -math.sin(angle), 0],
                    [0, math.sin(angle), math.cos(angle), 0],
                    [0, 0, 0, 1]
                ]
            )
        elif axis == "y" or axis == (0, 1, 0):
            
            return np.array(
                [
                    [math.cos(angle), 0, math.sin(angle), 0],
                    [0, 1, 0, 0],
                    [-math.sin(angle), 0, math.cos(angle), 0],
                    [0, 0, 0, 1]
                ]
            )
        elif axis == "z" or axis == (0, 0, 1):
            return np.array(
                [
                    [math.cos(angle), -math.sin(angle), 0, 0],
                    [math.sin(angle), math.cos(angle), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
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

        rotate_on_axis = MatrixHelper.getRotationMatrixByAngleAndAxis(angle, axis)

        matrices = [
            to_origin,
            rotate_on_axis,
            translate_back,
        ]
        result = np.eye(4)

        for n in range(len(matrices)):
            result = np.matmul(result, matrices[n])

        return result
    
    def calculateWindowRotationMatrix(obj : Shape, angle, axis,Wx,Wy,Wz):
        angle = math.radians(angle)
        center = obj.calcObjectCenter()
        x, y, z, o = center

        to_origin = MatrixHelper.getTranslationMatrix(-(x-(x-Wx)), -(y-(y-Wy)), -(z-Wz))

        translate_back = MatrixHelper.getTranslationMatrix((x-(x-Wx)), (y-(y-Wy)), z-Wz)

        rotate_on_axis = MatrixHelper.getRotationMatrixByAngleAndAxis(angle, axis)

        matrices = [
            to_origin,
            rotate_on_axis,
            translate_back,
        ]
        result = np.eye(4)

        for n in range(len(matrices)):
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
    
    def calculateWindowNormalizations(
        window_x_shift,
        window_y_shift,
        window_width,
        window_height,
        window_angle_x,
        window_angle_y,
        window_angle_z,
    ):
        translation_matrix = MatrixHelper.getTranslationMatrix(
            window_x_shift, window_y_shift, 0
        )
        rotation_matrix = MatrixHelper.getRotationMatrix(
            window_angle_x, window_angle_y, window_angle_z
        )

        scaling_matrix = MatrixHelper.getScaleMatrix(
            2 / window_width, 2 / window_height, 2 / window_width
        )

        composition = reduce(np.dot, [translation_matrix, rotation_matrix, scaling_matrix])

        return composition
