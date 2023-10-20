"""
RobotInfo.py

Centralized location to get information to connect to the robot

Created by Liam McKinney

Created 10/12/2023
Revised 10/19/2023
    -Added comments (Liam McKinney)
"""

# the IP/hostname of the robot
def getRobotIP():
    return "case.local"

# The port we connect to the robot with
def getPort():
    return 9559