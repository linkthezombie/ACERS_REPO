"""
Orientation.py

An orientation describes some rotation in 3D space
Why is this needlessly complicated when we could just use pitch, yaw, and roll?
https://github.com/moble/quaternion/wiki/Euler-angles-are-horrible

Created by Dylan Polson

Created 11/11/2023
"""

from dataclasses import dataclass
import numpy as np
import quaternion # numpy-quaternion package

from positioning.Vector3D import Vector3D

@dataclass
class Orientation:
    quaternion

    # Returns a base orientation
    def __init__(self):
        self.quaternion = np.quaternion(1.0, 0.0, 0.0, 0.0)

    # Constructs an orientation from an axis-angle representation
    # Angle is in radians.
    def fromAxisAngle(axis: Vector3D, angle: float):
        axis.normalize()
        axis.scale(angle)
        list_vector: list[float] = axis.getList()

        orientation = Orientation()
        orientation.quaternion = quaternion.from_rotation_vector(list_vector)
        return orientation

    # Constructs an orientation from an rotation matrix
    def fromRotationMatrix(rvec: list[list[float]]):
        orientation = Orientation()
        orientation.quaternion = quaternion.from_rotation_matrix(rvec)

        return orientation

    # Constructs an orientation from an rvec
    def fromRvec(rvec: list[list[float]]):
        return Orientation.fromRotationMatrix(rvec)

    # Gets the axis-angle representation of the orientation
    def getAxisAngle(self) -> (Vector3D, float):
        listVector: list[float] = quaternion.as_rotation_vector(self.quaternion)
        vector: Vector3D = Vector3D(listVector)
        rotation: float = vector.getLength()

        return (vector, rotation)

    # Gets a rotation matrix equivalent to the orientation
    def getRotationMatrix(self) -> list[list[float]]:
        return quaternion.as_rotation_matrix(self.quaternion)

    # Gets the rvec representation of the orientation
    def getRvec(self) -> list[list[float]]:
        return self.getRotationMatrix()

    # Creates an opposite orientation that undoes this one
    def invert(self):
        orientation = Orientation()
        orientation.quaternion = self.quaternion.inverse()

        return orientation

    # Rotates around the y-axis
    # Positive values will cause the orientation to pitch up
    def pitch(self, radians):
        q = quaternion.from_rotation_vector([0.0, -radians, 0.0])
        self.rotateQuaternion(q)

    # Rotates around the x-axis
    # Positive values will cause the orientation to roll to the right
    def roll(self, radians):
        q = quaternion.from_rotation_vector([radians, 0.0, 0.0])
        self.rotateQuaternion(q)

    # Changes the orientation by another orientation
    def rotate(self, other):
        self.quaternion *= other.quaternion

    # Changes the orientation by a raw quaternion
    def rotateQuaternion(self, quaternion):
        self.quaternion *= quaternion

    # Rotates a vector by this orientation
    def rotateVector(self, vector: Vector3D) -> Vector3D:
        wx = self.quaternion.w * vector.x + self.quaternion.y * vector.z - self.quaternion.z * vector.y
        wy = self.quaternion.w * vector.y + self.quaternion.z * vector.x - self.quaternion.x * vector.z
        wz = self.quaternion.w * vector.z + self.quaternion.x * vector.y - self.quaternion.y * vector.x

        x = vector.x + 2.0 * (self.quaternion.y * wz - self.quaternion.z * wy)
        y = vector.y + 2.0 * (self.quaternion.z * wx - self.quaternion.x * wz)
        z = vector.z + 2.0 * (self.quaternion.x * wy - self.quaternion.y * wx)

        return Vector3D([x, y, z])

    # Rotates around the z-axis
    # Positive values will cause the orientation yaw to the left
    def yaw(self, radians):
        q = quaternion.from_rotation_vector([0.0, 0.0, radians])
        self.rotateQuaternion(q)