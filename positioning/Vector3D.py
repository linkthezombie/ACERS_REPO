"""
Vector3D.py

A Vector3D holds a 3D vector, duh

Created by Dylan Polson

Created 11/11/2023
"""

from copy import copy, deepcopy
from math import sqrt

# Just makes sure values are all in the right places
# the NAOqi axes make a right handed coordinate system with
#     +x: out the front of the robot
#     +y: out the left of the robot
#     +z: up
class Vector3D:
    # self.x: float
    # self.y: float
    # self.z: float

    # Constructs from a 3 vec
	#
	# vector: list[float], [x, y, z]
    def __init__(self, vector):
        self.x, self.y, self.z = vector

    # Vector addition
	#
	# other: Vector3D, the RHS vector
	# returns a new added Vector3D
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z

        return Vector3D([x, y, z])

    # Vector addition
	#
	# other: Vector3D, the RHS vector
	# returns a new subtracted Vector3D
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z

        return Vector3D([x, y, z])

    # Gets the length from tail to tip
	#
	# returns a float
    def getMagnitude(self):
        x = self.x**2
        y = self.y**2
        z = self.z**2

        return sqrt(x + y + z)

    # Gets the vector as a list of floats
	#
	# returns list[float]
    def getList(self):
        return [copy(self.x), copy(self.y), copy(self.z)]

    # Returns a copy of this vector with a length of 1
	#
	# returns a new normalized Vcetor3D
    def normalize(self):
        length = self.getMagnitude()
        return self.scale(1.0 / length)

    # Returns a copy of this vector scaled by a scalar
	#
	# scaler: float
	# returns a new scaled Vector3D
    def scale(self, scalar):
        x = self.x * scalar
        y = self.y * scalar
        z = self.z * scalar

        return Vector3D([x, y, z])

    # Returns a copy of this vector with values swizzled to switch the coordinate
    # system's handedness around the Z axis.
    # I swear I didn't just make up a word https://en.wikipedia.org/wiki/Swizzling_(computer_graphics)
	#
	# returns a new swizzled Vector3D
    def swizzleHandedness(self):
        this = deepcopy(self)
        (this.x, this.y) = (self.y, self.x)

        return this
