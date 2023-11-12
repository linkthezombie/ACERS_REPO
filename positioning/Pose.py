"""
Pose.py

A Pose object holds a position and orientation to describe some object in space

Created by Dylan Polson

Created 11/11/2023
"""

from copy import deepcopy
from dataclasses import dataclass
import numpy as np

from positioning.Orientation import Orientation
from positioning.Vector3D import Vector3D


# Contains position and orientation information in 3D
@dataclass
class Pose:
    orientation: Orientation
    position: Vector3D

    # Constructs a new Pose from a position vector and quaternion for orientation
    def __init__(self, position: Vector3D, orientation: Orientation):
        self.position = position
        self.orientation = orientation

    # Returns a copy of this pose in coordinates based on the end of basePose
    def baseOn(self, basePose):
        # Orientation update
        this = deepcopy(self)
        that_orientation = deepcopy(basePose.orientation)
        that_orientation.rotate(self.orientation)
        this.orientation = that_orientation

        # Position update
        m = basePose.getTransformationMatrix()
        v = this.position

        # Assume a w value of 1 on input, then immediately discard resultant w
        this.position.x = v.x * m[0][0] + v.y * m[0][1] + v.z * m[0][2] + m[0][3]
        this.position.y = v.x * m[1][0] + v.y * m[1][1] + v.z * m[1][2] + m[1][3]
        this.position.z = v.x * m[2][0] + v.y * m[2][1] + v.z * m[2][2] + m[2][3]

        return this


    # Gets the origin pose
    def getNewOrigin():
        position = Vector3D([0.0, 0.0, 0.0])
        orientation = Orientation()
        return Pose(position, orientation)

    # Gets the transformation matrix (4x4) to get from the origin to this pose
    def getTransformationMatrix(self) -> list[list[float]]:
        v = self.position
        r = self.orientation.getRotationMatrix()

        return [[r[0][0], r[0][1], r[0][2], v.x],
                [r[1][0], r[1][1], r[1][2], v.y],
                [r[2][0], r[2][1], r[2][2], v.z],
                [0.0,     0.0,     0.0,     1.0]]

    # Rotates the orientation around by another orientation
    def rotate(self, orientation: Orientation):
        self.orientation.rotate(orientation)

    # Rotates the entire position around from the base
    def rotateFromBase(self, orientation: Orientation):
        raise NotImplementedError

    # Moves over by a translation vector
    def translate(self, translation: Vector3D):
        self.position += translation

    # Does the opposite of BaseOn
    # Useful if you have a value based on a camera that can move.
    # markerPos.unBaseOn(cameraPos) would get marker coordinates in world space.
    def unBaseOn(self, basePose):
        raise NotImplementedError
