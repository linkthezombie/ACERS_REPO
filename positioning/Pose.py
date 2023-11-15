"""
Pose.py

A Pose object holds a position and orientation to describe some object in space

Created by Dylan Polson

Created 11/11/2023
"""

from copy import deepcopy
from dataclasses import dataclass

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
        v = this.position - base.position
        print(v.getMagnitude())
        this.position = base.orientation.invert().rotateVector(v)

        return this

    # Gets the origin pose
    def getNewOrigin():
        position = Vector3D([0.0, 0.0, 0.0])
        orientation = Orientation()
        return Pose(position, orientation)

    # Rotates the orientation around by another orientation
    def rotate(self, orientation: Orientation):
        self.orientation.rotate(orientation)

    # Rotates the entire position around from the base
    def rotateFromBase(self, orientation: Orientation):
        raise NotImplementedError

    # Moves over by a translation vector
    def translate(self, translation: Vector3D):
        self.position += translation
