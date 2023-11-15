"""
Vector3D.py

A Vector3D holds a 3D vector, duh

Created by Dylan Polson

Created 11/11/2023
"""

from dataclasses import dataclass
from math import sqrt

# Just makes sure values are all in the right places
# the NAOqi axes make a right handed coordinate system with
#     +x: out the front of the robot
#     +y: out the left of the robot
#     +z: up
@dataclass
class Vector3D:
    x: float
    y: float
    z: float

    # Constructs from a 3 vec
    def __init__(self, vector: list[float]):
        self.x, self.y, self.z = vector

    # Vector addition
    def __add__(self, other):
        x: float = self.x + other.x
        y: float = self.y + other.y
        z: float = self.z + other.z

        return Vector3D([x, y, z])

    # Gets the length from tail to tip
    def getMagnitude(self) -> float:
        x = self.x**2
        y = self.y**2
        z = self.z**2

        return sqrt(x + y + z)

    # Gets the vector as a list of floats
    def getList(self) -> list[float]:
        return [self.x, self.y, self.z]

    # Normalizes the vector so the length is 1
    def normalize(self):
        length = self.getMagnitude()
        self.scale(1 / length)

    # Scales this vector by a scalar value
    def scale(self, scalar: float):
        self.x = self.x * scalar
        self.y = self.y * scalar
        self.z = self.z * scalar

    # Swizzles values to switch the coordinate system's handedness around the Z axis
    # I swear I didn't just make up a word https://en.wikipedia.org/wiki/Swizzling_(computer_graphics)
    def swizzleHandedness(self):
        (self.x, self.y) = (self.y, self.x)
