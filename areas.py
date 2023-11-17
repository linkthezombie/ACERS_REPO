"""
areas.py

Defines the areas of play in ArUco marker coordinates

Created by Dylan Polson

Created 11/14/2023
"""

from positioning.Orientation import Orientation
from positioning.Pose import Pose
from positioning.RectangularVolume import RectangularVolume
from positioning.Vector3D import Vector3D

# These areas have NOT been tested with an actual robot. Since they're dependent
# on ArUco coordinates, they may even change between runs. We may want to eventually
# use Pose's coordinate transformations to get world oriented coordinates if this
# does not work.
areas = [
    ("discard pile", RectangularVolume(
        Pose(
            Vector3D([0.23672599, 0.03968427, -0.03701625]), # Position
            Orientation.fromRvec([[-0.0401685,  -0.99880221, -0.02795802], # Orientation
                                  [ 0.99905071, -0.03967498, -0.01798863],
                                  [ 0.01685785, -0.02865405,  0.99944772]])
        ),
        Vector3D([0.1, 0.07, 0.127])) # Size
    ),
    # ("draw pile", ), no data for this
    # ("hand", ), no data for this
    ("in your face", RectangularVolume(
        Pose(
            Vector3D([0.13677668, 0.02042692, 0.12778244]), # Position
            Orientation.fromRvec([[-0.3269222, -0.11921903, -0.93750184], # Orientation
                                  [-0.19346542, 0.97944479, -0.05708824],
                                  [ 0.92503727, 0.16271077, -0.34326699]])
        ),
        Vector3D([0.0, 0.0, 0.0])) # Size NOT SET, I have no guess as to the size of this
    ),
]

# Finds which area this pose is in
# If it is in a defined area, return the corresponding string, otherwise return None
def findPlayArea(pose):
    for (name, area) in areas:
        if area.contains(pose):
            return name

    return None
