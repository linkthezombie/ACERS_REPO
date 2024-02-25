"""
Orientation.py

An orientation describes some rotation in 3D space
Why is this needlessly complicated when we could just use pitch, yaw, and roll?
https://github.com/moble/quaternion/wiki/Euler-angles-are-horrible

Created by Dylan Polson

Created 11/11/2023
"""

from math import acos, cos, sin, sqrt

from positioning.Quaternion import *
from positioning.Vector3D import Vector3D

class Orientation:
    # quaternion: Quaternion

    # Returns a base orientation
    def __init__(self):
        self.quaternion = Quaternion(1.0, 0.0, 0.0, 0.0)

    # Constructs an orientation from an axis-angle representation
    # Angle is in radians.
    #
    # axis: Vector3D, the axis around which the rotation occurs
    # angle: float, the angle of the rotation
    # returns a new Orientation
    @staticmethod
    def fromAxisAngle(axis, angle):
        a = axis.normalize().getList()
        x = a[0] * sin(angle / 2)
        y = a[1] * sin(angle / 2)
        z = a[2] * sin(angle /2 )
        w = cos(angle / 2)

        orientation = Orientation()
        orientation.quaternion = Quaternion(w, x, y, z)

        return orientation

    # Constructs an orientation from an rotation matrix
    #
    # rvec: list[list[float]], the rotation matrix
    # returns a new Orientation
    @staticmethod
    def fromRotationMatrix(m):
        w = sqrt(1.0 + m[0][0] + m[1][1] + m[2][2]) / 2.0
        x = (m[2][1] - m[1][2]) / ( 4.0 * w)
        y = (m[0][2] - m[2][0]) / ( 4.0 * w)
        z = (m[1][0] - m[0][1]) / ( 4.0 * w)

        orientation = Orientation()
        orientation.quaternion = Quaternion(w, x, y, z)
        return orientation

    # Constructs an orientation from an rvec
    #
    # rvec: list[list[float]], the rvec
    # returns a new Orientation
    @staticmethod
    def fromRvec(rvec):
        return Orientation.fromRotationMatrix(rvec)

    # Gets the axis-angle representation of the orientation
    #
    # returns (axis: Vector3D, angle: float)
    def getAxisAngle(self):
        q = self.quaternion

        angle = 2 * acos(q.w)
        x = q.x / sqrt(1 - q.w ** 2)
        y = q.y / sqrt(1 - q.w ** 2)
        z = q.z / sqrt(1 - q.w ** 2)

        return (Vector3D([x, y, z]), angle)

    # Gets a rotation matrix equivalent to the orientation
    #
    # returns list[list[float]]
    def getRotationMatrix(self):
        q = self.quaternion
        n = q.norm()

        # This isn't going to work with a 0 norm quaternion
        if n == 0.0: raise ZeroDivisionError("Tried to use quaternion with zero norm to create rotation matrix")

        return [
            [1 - 2 * (q.y ** 2  + q.z ** 2)  / n,     2 * (q.x * q.y - q.z * q.w) / n,     2 * (q.x * q.z + q.y * q.w) / n],
            [    2 * (q.x * q.y + q.z * q.w) / n, 1 - 2 * (q.x ** 2  + q.z ** 2)  / n,     2 * (q.y * q.z - q.x * q.w) / n],
            [    2 * (q.x * q.z - q.y * q.w) / n,     2 * (q.y * q.z + q.x * q.w) / n, 1 - 2 * (q.x ** 2  + q.y ** 2)  / n]
        ]

    # Gets the rvec representation of the orientation
    #
    # returns list[list[float]], the rotation matrix
    def getRvec(self):
        return self.getRotationMatrix()

    # Creates an opposite orientation that undoes this one
    #
    # returns a new Orientation
    def invert(self):
        orientation = Orientation()
        orientation.quaternion = self.quaternion.inverse()

        return orientation

    # Rotates around the y-axis
    # Positive values will cause the orientation to pitch up
    #
    # radians: float
    # returns a new Orientation
    def pitch(self, radians):
        orientation = Orientation.fromAxisAngle(Vector3D([0.0, -1.0, 0.0]), radians)
        return self.rotate(orientation)

    # Rotates around the x-axis
    # Positive values will cause the orientation to roll to the right
    #
    # radians: float
    # returns a new Orientation
    def roll(self, radians):
        orientation = Orientation.fromAxisAngle(Vector3D([1.0, 0.0, 0.0]), radians)
        return self.rotate(orientation)

    # Returns a copy of this orientation rotated by another orientation
    def rotate(self, other):
        return self.rotateQuaternion(other.quaternion)

    # Returns a copy of this orientation rotated by a raw quaternion
    def rotateQuaternion(self, quaternion):
        orientation = Orientation()
        orientation.quaternion = self.quaternion * quaternion

        return orientation

    # Rotates a vector by this orientation
    #
    # vector: Vector3D, the vector to be rotated
    # returns a new rotated Vector3D
    def rotateVector(self, vector):
        wx = self.quaternion.w * vector.x + self.quaternion.y * vector.z - self.quaternion.z * vector.y
        wy = self.quaternion.w * vector.y + self.quaternion.z * vector.x - self.quaternion.x * vector.z
        wz = self.quaternion.w * vector.z + self.quaternion.x * vector.y - self.quaternion.y * vector.x

        x = vector.x + 2.0 * (self.quaternion.y * wz - self.quaternion.z * wy)
        y = vector.y + 2.0 * (self.quaternion.z * wx - self.quaternion.x * wz)
        z = vector.z + 2.0 * (self.quaternion.x * wy - self.quaternion.y * wx)

        return Vector3D([x, y, z])

    # Rotates around the z-axis
    # Positive values will cause the orientation yaw to the left
    #
    # radians: float
    # returns a new Orientation
    def yaw(self, radians):
        orientation = Orientation.fromAxisAngle(Vector3D([0.0, 0.0, 1.0]), radians)
        return self.rotate(orientation)
