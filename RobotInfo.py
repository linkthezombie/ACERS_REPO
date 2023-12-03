"""
RobotInfo.py

Centralized location to get information to connect to the robot

Created by Liam McKinney

Created 10/12/2023
Revised 10/19/2023
    -Added comments (Liam McKinney)
Revised 12/3/2023
    -Added use of a config file to support multiple robots
"""
import json

cfg = None
with open("config.json") as f:
    cfg = json.load(f)
# the IP/hostname of the robot
def getRobotIP():
    return str(cfg["hostname"])

# The port we connect to the robot with
def getPort():
    return cfg["port"]