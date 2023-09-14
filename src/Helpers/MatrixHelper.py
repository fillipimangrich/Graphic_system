import numpy as np
import math
from functools import reduce

from src.shapes.Shape import Shape


class MatrixHelper():

    def getRotationMatrix(dX, dY, dZ):
        """
        Build rotation matrix as composition from:

        Rx = [1  0       0       0]
            [0  cos(dX) sen(dX) 0]
            [0 -sen(dX) cos(dX) 0]
            [0  0       0       1]

        Ry = [cos(dY) 0 -sen(dY) 0]
            [0       1 0        0]
            [sen(dY) 0 cos(dY)  0]
            [0       0 0        1]

        Rz = [cos(dZ)  sen(dZ) 0 0]
            [-sen(dZ) cos(dZ) 0 0]
            [0        0       1 0]
            [0        0       0 1]
        """
        Rx = np.identity(4)
        Rx[1][1] = np.cos(np.deg2rad(dX))
        Rx[1][2] = np.sin(np.deg2rad(dX))
        Rx[2][1] = -np.sin(np.deg2rad(dX))
        Rx[2][2] = np.cos(np.deg2rad(dX))

        Ry = np.identity(4)
        Ry[0][0] = np.cos(np.deg2rad(dY))
        Ry[0][2] = -np.sin(np.deg2rad(dY))
        Ry[2][0] = np.sin(np.deg2rad(dY))
        Ry[2][2] = np.cos(np.deg2rad(dY))

        Rz = np.identity(4)
        Rz[0][0] = np.cos(np.deg2rad(dZ))
        Rz[0][1] = np.sin(np.deg2rad(dZ))
        Rz[1][0] = -np.sin(np.deg2rad(dZ))
        Rz[1][1] = np.cos(np.deg2rad(dZ))

        return reduce(np.dot, [Rx, Ry, Rz])


    def getRotationMatrixByAngleAndAxis(angle, axis):
        if axis == "x" or axis == (1, 0, 0):
            return np.array(
                [
                    [math.cos(angle), -math.sin(angle), 0, 0],
                    [math.sin(angle), math.cos(angle), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ]
            )
        elif axis == "y" or axis == (0, 1, 0):
            angle = angle + 90
            return np.array(
                [
                    [math.cos(angle), -math.sin(angle), 0, 0],
                    [math.sin(angle), math.cos(angle), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ]
            )
        elif axis == "z" or axis == (0, 0, 1):
            return np.array(
                [
                    [math.cos(angle), math.sin(angle), 0, 0],
                    [-math.sin(angle), math.cos(angle), 0, 0],
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

        vector = obj.get_axis_vector(axis)

        beta_on_yz = obj.getBetaOnYz(vector.copy())

        beta_on_xy = obj.getBetaOnXy(vector.copy())

        rotate_to_xy = MatrixHelper.getRotationMatrixByAngleAndAxis(beta_on_yz, "x")
        rotate_from_xy = MatrixHelper.getRotationMatrixByAngleAndAxis(-beta_on_yz, "x")

        rotate_to_y = MatrixHelper.getRotationMatrixByAngleAndAxis(beta_on_xy, "z")
        rotate_from_y = MatrixHelper.getRotationMatrixByAngleAndAxis(-beta_on_xy, "z")

        rotate_on_y = MatrixHelper.getRotationMatrixByAngleAndAxis(angle, "y")

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
