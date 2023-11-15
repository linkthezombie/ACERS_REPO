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

    # Adds this Pose on top of a base Pose. Inverse of changeOrigin.
    # This is useful to get a Pose in world oriented coordinates. If you know where
    # the robot is in the world, and you know where your hand is relative to the
    # robot, you can find the hand relative to the world.
    def addOnto(self, base):
        # Orientation update
        this = deepcopy(self)
        thatOrientation = deepcopy(base.orientation)
        thatOrientation.rotate(self.orientation)
        this.orientation = thatOrientation

        # Position update
        v = base.orientation.rotateVector(this.position)
        this.position = base.position + v

        return this

    # Takes another Pose with the same origin as this one
    # Returns a new Pose with base as its origin.
    # This can be useful for abstracting away how the rest of the body is moving,
    # and focusing on something in base's frame of reference.
    def changeOrigin(self, base):
        # Orientation update
        this = deepcopy(self)
        inverse = base.orientation.invert()
        inverse.rotate(this.orientation)
        this.orientation = inverse

        # Position update
        print(Vector3D([6.0, 5.0, 4.0]).getMagnitude())
        # this.position = self.orientation.invert().rotateVector(this.position)

        # print(max(self.position.x - this.position.x, self.position.y - this.position.y, self.position.z - this.position.z))

        v = this.position - base.position
        print(v.getMagnitude())
        this.position = base.orientation.invert().rotateVector(v)
        # this.position = Vector3D([x, y, z])

        # this.position = Vector3D([x, y, z])
        # print(this.position.getMagnitude())

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
