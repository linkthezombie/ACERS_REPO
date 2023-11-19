"""
RobotMotion.py

Helper functions to execute several motions on the robot,
ranging from simple adjustments to sequences of game actions

Created by Liam McKinney

Created 10/19/2023

Revised 11/1/2023
  -Refined draw animation
  -Reworked and separated handoff & put in tray into two separate motions

Revised 11/19/2023
  -Implemented card checking during handOffLtoR
"""
import time
from naoqi import ALProxy
import RobotInfo
import ComputerVision

d2r = 3.14159 / 180

# percent of max speed to be used for most animations
pctMax = .35

motion = ALProxy("ALMotion", RobotInfo.getRobotIP(), RobotInfo.getPort())

# predefined positions for drawing/playing Cards
realStart = [0.1548919677734375, -0.07060599327087402, -90 * d2r, -0.03490658476948738, 90 * d2r, .65]

holderPlacement = [-0.0827939, -0.25622, 0.246933, 0.325249, -0.0506639, 0.27]

centerCardL = [-0.0445281, 0.360449, -0.243948, -1.36368, -1.17048, 0.28]
centerCardR = [0.1, -0.299172, 0.246933, 1.31928, 1.21489, 1]

# Draw a card from the top of the stack into Ace's left hand.
def drawCard():
    # starting position
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

    # Move the hand forward to position the thumb under the card so it can grab
    motion.changePosition("LArm", 0, [.02, 0, 0, 0, 0, 0], pctMax, 7)
    time.sleep(1)

    # grab the card
    motion.setAngles("LHand", .29, pctMax)
    time.sleep(1)

    # pull the card the rest of the way out
    motion.changeAngles("LElbowRoll", -20 * d2r, pctMax)
    time.sleep(1)

    # Rotate the hand 180 degrees to remove the card from the tray completely
    motion.setAngles("LWristYaw", -100 * d2r, pctMax)
    time.sleep(1)

# Assuming a card is in Ace's left hand, hand it off to the right hand
def handOffLtoR():
    # Move the left hand to center the card in front of Ace's chest
    motion.setAngles("LArm", centerCardL, pctMax)
    time.sleep(1.5)

    # Check what card we drew, if we can see the marker
    ids, xs, Rs = ComputerVision.getVisibleCards()
    drawnCard = ComputerVision.getDrawnCard(ids, xs, Rs)

    # Make a copy of the right arm pose
    upperPos = centerCardR[:]
    # Adjust shoulder to be further out to the side
    upperPos[1] = -60 * d2r

    # put right hand to the right of the card, so we can move the hand in without colliding with the card
    motion.setAngles("RArm", upperPos, pctMax)
    time.sleep(1.5)

    # move the right hand in, so it can grab the card.
    motion.setAngles("RShoulderRoll", centerCardR[1], pctMax)
    time.sleep(1)

    # Loosen left hand grip so right hand can "pull it out" as it grabs the card.
    motion.setStiffnesses("LHand", .5)

    # Grab the card with the right hand
    motion.setAngles("RHand", .27, pctMax)
    time.sleep(.5)

    # Release with the left hand
    motion.setAngles("LHand", 1, pctMax)
    time.sleep(.5)

    # Move left arm out of the way, and restore the hand's stiffness
    motion.setAngles("LShoulderRoll", 60 * d2r, pctMax)
    motion.setStiffnesses("LHand", 1)
    time.sleep(1)

    #TODO check card again; other corner should be visible now

# Assuming the card is in Ace's right hand, put it into the tray at in the [offset]th position
def placeCardInHolder(offset):
    targetPos = holderPlacement[:]

    targetPos[1] -= 10 * d2r * offset

    motion.setAngles("RArm", targetPos, pctMax)
    time.sleep(1)

    motion.setAngles("RHand", 1, pctMax)
    time.sleep(.5)