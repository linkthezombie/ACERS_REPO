"""
RobotMotion.py

Helper functions to execute several motions on the robot,
ranging from simple adjustments to sequences of game actions

Created by Liam McKinney

Created 10/19/2023
"""
import time
from naoqi import ALProxy
import RobotInfo

d2r = 3.14159 / 180

# percent of max speed to be used for most animations
pctMax = .35

motion = ALProxy("ALMotion", RobotInfo.getRobotIP(), RobotInfo.getPort())

# predefined positions for drawing/playing Cards
drawStart = [0.015298128128051758, -0.09668397903442383, -0.19485998153686523, -0.14568805694580078, 0.015298128128051758, 0.7135999798774719]
newStart = [0.11347413063049316, -0.12276196479797363, -1.5355758666992188, -0.08893013000488281, 1.3851600885391235, 0.722000002861023]

startPos6d = [0.2145160734653473, 0.09448506683111191, 0.053448572754859924, 0, 0.14129656553268433, -0.07788744568824768]

realStart = [0.1548919677734375, -0.07060599327087402, -90 * d2r, -0.03490658476948738, 90 * d2r, .65]
# gently rest a hand onto whatever surface it's hovering above
#def restHand():
#   # loosen shoulder joint, allowing it to fall
#   motion.setStiffnesses("LShoulderPitch", 0)
#   # wait for it to fall, then set the arm's target to wherever it fell to
#   time.sleep(.75)
#   motion.setAngles("LArm", motion.getAngles("LArm", True), pctMax)
#   # give Nao a bit of time to process the new target position
#   time.sleep(.2)
#   # stiffen the shoulder again for future motion
#   motion.setStiffnesses("LShoulderPitch", 1)
#
## grab the top card of the deck, assuming the robot's hand is resting on the deck
#
## TODO needs work. Maybe reduce hand stiffness when dragging?
#def grabCard():
#    names = list()
#    times = list()
#    keys = list()
#    #pull hand up and back as we curl the fingers
#    motion.changePosition("LArm", 0, [-.03, 0, 0, 0, 0, 0], pctMax, 63)
#    time.sleep(1)
#    motion.setAngles("LHand", .29, pctMax)


def drawCard():
    motion.setAngles("LArm", realStart, pctMax)
    time.sleep(1)

    # Allow the elbow to bend freely so we can easily "drag" the hand along the deck
    motion.setStiffnesses("LElbowRoll", 0)
    # slowly lower the shoulder to drag the hand along the top of the deck, separating the top card
    motion.changeAngles("LShoulderPitch", 40 * d2r, .1)
    time.sleep(1.5)

    motion.setStiffnesses("LElbowRoll", 1)
    time.sleep(.5)
    # Lift the elbow slightly to get the hand in better grabbing position
    motion.changeAngles("LElbowRoll", -15 * d2r, .1)
    time.sleep(1)

    motion.changePosition("LArm", 0, [.02, 0, 0, 0, 0, 0], pctMax, 7)
    time.sleep(1)

    #grab the card
    motion.setAngles("LHand", .29, pctMax)
    time.sleep(1)

    #pull the card the rest of the way out
    motion.changeAngles("LElbowRoll", -20 * d2r, pctMax)
    time.sleep(1)

    motion.setAngles("LWristYaw", -100 * d2r, pctMax)

# assuming a card is in Ace's left hand, pass it off to the right hand and place it in the card holder at the specified position
frameTimes = [2, 3, 4, 5, 7, 8, 9]
def putCardInHolder(offset):
    # Choregraphe simplified export in Python.
    names = list()
    times = list()
    keys = list()

    #[1, 1.4, 2, 2.6, 4.2, 4.8]

    names.append("LElbowRoll")
    times.append(frameTimes)
    keys.append([-1.36368, -1.36368, -1.36368, -1.36368, -1.36368, -1.36368, -1.36368])

    names.append("LElbowYaw")
    times.append(frameTimes)
    keys.append([-0.243948, -0.243948, -0.243948, -0.243948, -0.243948, -0.243948, -0.243948])

    names.append("LHand")
    times.append(frameTimes)
    keys.append([0.28, 0.28, 0.28, 1, 0.9924, 0.9924, 0.9924])

    names.append("LShoulderPitch")
    times.append(frameTimes)
    keys.append([-0.0445281, -0.0445281, -0.0445281, -0.0445281, -0.0445281, -0.0445281, -0.0445281])

    names.append("LShoulderRoll")
    times.append(frameTimes)
    keys.append([0.360449, 0.360449, 0.360449, 0.360449, 0.360449, 0.360449, 0.360449])

    names.append("LWristYaw")
    times.append(frameTimes)
    keys.append([-1.17048, -1.17048, -1.17048, -1.17048, -1.17048, -1.17048, -1.17048])

    names.append("RElbowRoll")
    times.append(frameTimes)
    keys.append([1.31928, 1.31928, 1.31928, 1.29014, 0.326598, 0.325249, 0.325249])

    names.append("RElbowYaw")
    times.append(frameTimes)
    keys.append([0.246933, 0.246933, 0.246933, 0.246933, 0.246933, 0.246933, 0.246933])

    names.append("RHand")
    times.append(frameTimes)
    keys.append([1, 0.29, 0.29, 0.29, 0.29, 0.29, 0.9868])

    names.append("RShoulderPitch")
    times.append(frameTimes)
    keys.append([-0.0199001, -0.0199001, -0.0199001, -0.0199001, -0.161893, -0.0827939, -0.0827939])

    names.append("RShoulderRoll")
    times.append(frameTimes)
    keys.append([-0.299172, -0.299172, -0.299172, -0.299172, -0.299172, -0.25622, -0.25622])

    names.append("RWristYaw")
    times.append(frameTimes)
    keys.append([1.21489, 1.21489, 1.21489, 1.21489, -0.110265, -0.0506639, -0.0506639])

    try:
        # uncomment the following line and modify the IP if you use this script outside Choregraphe.
        motion.angleInterpolation(names, keys, times, True)
    except BaseException, err:
        print err

