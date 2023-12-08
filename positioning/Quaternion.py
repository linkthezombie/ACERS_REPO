"""
Quaternion.py

It's dark magic.

Created by Dylan Polson

Created 12/07/2023
"""

from math import cos, exp, sin, sqrt

class Quaternion:
    # w: float, real part
    # x: float, first imaginary part
    # y: float, second imaginary part
    # z: float, third imaginary part

    # Construct a new Quaternion from its parts
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    # Multiply two quaternions
    def __mul__(self, other):
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w

        return Quaternion(w, x, y, z)

    def exp(self):
        iMag = sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

        # If the imaginary part's magnitude is zero, skip the math
        if iMag < 1e-14: return Quaternion(exp(self.w), 0.0, 0.0, 0.0)

        s = sin(iMag) / iMag
        e = exp(self.w)

        w = e * cos(iMag)
        x = e * s * self.x
        y = e * s * self.y
        z = e * s * self.z

        return Quaternion(w, x, y, z)

    def inverse(self):
        n = self.norm()
        return Quaternion(self.w / n, -self.x / n, -self.y / n, -self.z / n)

    def norm(self):
        return self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2
