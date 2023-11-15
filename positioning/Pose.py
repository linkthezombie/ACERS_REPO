"""
Pose.py

A Pose object holds a position and orientation to describe some object in space

Created by Dylan Polson

Created 11/11/2023
"""

from copy import copy
from dataclasses import dataclass

from positioning.Orientation import Orientation
from positioning.Vector3D import Vector3D

# Contains position and orientation information in 3D
class Pose:
    # self.orientation: Orientation
    # self.position: Vector3D

    # Constructs a new Pose from a position vector and quaternion for orientation
	#
	# position: Vector3D
	# orientation: Orientation
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

    # Adds this Pose on top of a base Pose. Inverse of changeOrigin.
    # This is useful to get a Pose in world oriented coordinates. If you know where
    # the robot is in the world, and you know where your hand is relative to the
    # robot, you can find the hand relative to the world.
	#
	# base: Pose, the Pose to stick self on top of
	# returns a new Pose
    def addOnto(self, base):
        # Orientation update
        orientation = base.orientation.rotate(self.orientation)

        # Position update
        v = base.orientation.rotateVector(self.position)
        position = base.position + v

        return Pose(position, orientation)

    # Takes another Pose with the same origin as this one
    # Returns a new Pose with base as its origin.
    # This can be useful for abstracting away how the rest of the body is moving,
    # and focusing on something in base's frame of reference.
	#
	# base: Pose, the new origin
	# returns a new Pose
    def changeOrigin(self, base):
        # Orientation update
        orientation = base.orientation.invert().rotate(self.orientation)

        # Position update
        v = self.position - base.position
        position = base.orientation.invert().rotateVector(v)

        return Pose(position, orientation)

    # Returns a new Pose at the origin
    def getNewOrigin():
        position = Vector3D([0.0, 0.0, 0.0])
        orientation = Orientation()
        return Pose(position, orientation)

    # Rotates the end orientation around
    #
    # orientation: Orientation
    # returns a new Pose
    def rotate(self, orientation):
        position = copy(self.position)
        orientation = self.orientation.rotate(orientation)
        return Pose(position, orientation)

    # Rotates the entire pose and position around from the origin
    #
    # orientation: Orientation
    # returns a new Pose
    def rotateAtOrigin(self, orientation):
        base = Pose.getNewOrigin().rotate(orientation)
        return self.addOnto(base)

    # Moves over by a translation vector
    #
    # translation: Vector3D
    # returns a new Pose
    def translate(self, translation):
        position = self.position + translation
        orientation = copy(self.orientation)
        return Pose(position, orientation)
