"""
RectangularVolume.py

A RectangularVolume is a simple rectangular prism with some pose

Created by Dylan Polson

Created 11/14/2023
"""

from positioning.Pose import Pose
from positioning.Vector3D import Vector3D

# A simple rectangular prism with some pose
# The pose should be in the center of the volume in xy, sitting at the bottom in z
class RectangularVolume:
    # pose: Pose
    # size: Vector3D

	# Initialize a new volume with a size at a given pose
	#
	# pose: Pose, The bottom center of the volume
	# size: Vector3D, the full dimensions of the volume
    def __init__(self, pose, size):
        self.pose = pose
        self.size = size

    # Checks to see if a given pose is inside this volume
    def contains(self, pose):
        correctedPose = pose.changeOrigin(self.pose)

        if correctedPose.position.x > self.size.x / 2.0:  return False
        if correctedPose.position.x < -self.size.x / 2.0: return False
        if correctedPose.position.y > self.size.x / 2.0:  return False
        if correctedPose.position.y < -self.size.x / 2.0: return False
        if correctedPose.position.z < 0.0:                return False
        if correctedPose.position.z > self.size.z:        return False
        return True
