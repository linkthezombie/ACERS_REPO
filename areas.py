"""
areas.py

Defines the areas of play in ArUco marker coordinates

Created by Dylan Polson

Created 11/14/2023

Edited 2/12/24 - Liam McKinney
  - Added Left and Right Stack zones.
"""

from positioning.Orientation import Orientation
from positioning.Pose import Pose
from positioning.RectangularVolume import RectangularVolume
from positioning.Vector3D import Vector3D

# bottom left: [array([ 0.17011172,  0.19805465, -0.03381562]), array([ 0.12591172,  0.25621441, -0.03891594])]
# top right: [array([0.19824349, 0.17826645, 0.02497191]), array([0.16223792, 0.24173862, 0.01945529])]
#array([0.2050575 , 0.16273877, 0.01744545]), array([0.16325731, 0.2397359 , 0.01290505])]
# These areas have NOT been tested with an actual robot. Since they're dependent
# on ArUco coordinates, they may even change between runs. We may want to eventually
# use Pose's coordinate transformations to get world oriented coordinates if this
# does not work.
areas = [
    #("discard pile", RectangularVolume(
    #    Pose(
    #        Vector3D([0.23672599, 0.03968427, -0.03701625]), # Position
    #        Orientation.fromRvec([[-0.0401685,  -0.99880221, -0.02795802], # Orientation
    #                              [ 0.99905071, -0.03967498, -0.01798863],
    #                              [ 0.01685785, -0.02865405,  0.99944772]])
    #    ),
    #    Vector3D([0.1, 0.07, 0.127])) # Size
    #),
    ("discard pile", RectangularVolume(
        Pose(
            Vector3D([0.24, .018, -.1]), # Position
            Orientation()
        ),
        Vector3D([.2, .2, .1])) # Size
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

    ("L Stack", RectangularVolume(
        Pose(
            Vector3D([ 0.14,  0.25, -0.06]), # Position
            Orientation()
        ),
        Vector3D([ .08, .08, .1])
    )),

    ("R Stack", RectangularVolume(
        Pose(
            Vector3D([ 0.185,  0.17, -0.05]), # Position
            Orientation()
        ),
        Vector3D([ .07, .08, .1])
    )),
]

# Finds which area this pose is in
# If it is in a defined area, return the corresponding string, otherwise return None
def findPlayArea(pose):
    for (name, area) in areas:
        if area.contains(pose):
            return name

    return None
