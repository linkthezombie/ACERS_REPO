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
	#
	# axis: Vector3D, the axis around which the rotation occurs
	# angle: float, the angle of the rotation
	# returns a new Orientation
    def fromAxisAngle(axis, angle):
        list_vector = axis.normalize().scale(angle).getList()

        orientation = Orientation()
        orientation.quaternion = quaternion.from_rotation_vector(list_vector)
        return orientation

    # Constructs an orientation from an rotation matrix
	#
	# rvec: list[list[float]], the rotation matrix
	# returns a new Orientation
    def fromRotationMatrix(rvec):
        orientation = Orientation()
        orientation.quaternion = quaternion.from_rotation_matrix(rvec)

        return orientation

    # Constructs an orientation from an rvec
	#
	# rvec: list[list[float]], the rvec
	# returns a new Orientation
    def fromRvec(rvec):
        return Orientation.fromRotationMatrix(rvec)

    # Gets the axis-angle representation of the orientation
	#
	# returns (axis: Vector3D, angle: float)
    def getAxisAngle(self):
        listVector = quaternion.as_rotation_vector(self.quaternion)
        vector = Vector3D(listVector)
        rotation = vector.getMagnitude()

        return (vector, rotation)

    # Gets a rotation matrix equivalent to the orientation
	#
	# returns list[list[float]]
    def getRotationMatrix(self):
        return quaternion.as_rotation_matrix(self.quaternion)

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
        q = quaternion.from_rotation_vector([0.0, -radians, 0.0])
        return self.rotateQuaternion(q)

    # Rotates around the x-axis
    # Positive values will cause the orientation to roll to the right
	#
	# radians: float
	# returns a new Orientation
    def roll(self, radians):
        q = quaternion.from_rotation_vector([radians, 0.0, 0.0])
        return self.rotateQuaternion(q)

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
        q = quaternion.from_rotation_vector([0.0, 0.0, radians])
        return self.rotateQuaternion(q)
