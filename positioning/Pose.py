"""
Pose.py

A Pose object holds a position and orientation to describe some object in space

Created by Dylan Polson

Created 11/11/2023
"""

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
        raise NotImplementedError

    # Gets the origin pose
    def getNewOrigin():
        position = Vector3D([0.0, 0.0, 0.0])
        orientation = Orientation()
        return Pose(position, orientation)

    # Gets the transformation matrix to get from the origin to this pose
    def getTransformationMatrix(self) -> list[list[float]]:
        raise NotImplementedError

    # Rotates the orientation around by another orientation
    def rotate(self, orientation: Orientation):
        self.orientation.rotate(orientation)

    # Moves over by a translation vector
    def translate(self, translation: Vector3D):
        self.position += translation

    # Does the opposite of BaseOn
    # Useful if you have a value based on a camera that can move.
    # markerPos.unBaseOn(cameraPos) would get marker coordinates in world space.
    def unBaseOn(self, basePose):
        raise NotImplementedError
