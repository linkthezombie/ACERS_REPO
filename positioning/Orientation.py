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
        self.orientation = np.quaternion(1.0, 0.0, 0.0, 0.0)

    # Constructs an orientation from an axis-angle representation
    # Angle is in radians.
    def fromAxisAngle(axis: Vector3D, angle: float):
        raise NotImplementedError

    # Constructs an orientation from an rvec
    # An rvec is like an axis-angle representation, but uses two orthogonal vectors
    # to describe rotation.
    def fromRvec(rvec: list[list[float]]):
        raise NotImplementedError

    # Gets the axis-angle representation of the orientation
    def getAxisAngle(self) -> (Vector3D, float):
        raise NotImplementedError

    # Gets Euler angle representation of the orientation (pitch, yaw, roll)
    def getEulerAngles(self) -> (float, float, float):
        raise NotImplementedError

    # Gets a rotation matrix equivalent to the orientation
    def getRotationMatrix(self) -> list[list[float]]:
        raise NotImplementedError

    # Gets the rvec representation of the orientation
    def getRvec(self) -> list[list[float]]:
        raise NotImplementedError

    # Rotates this orientation counter-clockwise around the z-axis
    def pitch(self, radians):
        raise NotImplementedError

    # Changes the orientation by a quaternion
    def rotate(orientation):
        raise NotImplementedError

    # Rotates this orientation counter-clockwise around the x-axis
    def roll(self, radians):
        raise NotImplementedError

    # Rotates a vector by this orientation
    def rotateVector(self, vector: Vector3D) -> Vector3D:
        raise NotImplementedError

    # Rotates this orientation counter-clockwise around the z-axis
    def yaw(self, radians):
        raise NotImplementedError