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
import AbstractionLayer
import numpy as np
import almath
from positioning.Pose import *
import ComputerVision


absLayer = AbstractionLayer.AbstractionLayer()

d2r = 3.14159 / 180

# percent of max speed to be used for most animations
pctMax = .35

motion = ALProxy("ALMotion", RobotInfo.getRobotIP(), RobotInfo.getPort())

# predefined positions for drawing/playing Cards

# Joint order: ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand']
realStart = [0.1548919677734375, -0.07060599327087402, -90 * d2r, -0.03490658476948738, 90 * d2r, .65]

holderPlacement = [-0.0827939, -0.25622, 0.246933, 0.325249, -0.246933, 0.27]

# offset to the holderPlacement position to "pull back" the card slightly
trayPlaceOffset = [0, -30*d2r, 0, 30*d2r, 0, 0]

centerCardL = [-0.0445281, 0.3, -0.243948, -1.36368, -1.17048, 0.28]
centerCardR = [0, -0.299172, 0.246933, 1.31928, 1.21489, .28]

# hand tracker

# while the virtual model knows which cards are in its hand, we have to maintain a separate copy here
# to track where in the holder each card is placed
hand = [None]

def wakeRobot():
    motion.wakeUp()
    readyArms()

def readyArms():
    motion.setAngles("LShoulderRoll", 1.25, pctMax)
    motion.setAngles("RShoulderRoll", -1.25, pctMax)
    time.sleep(.5)

    motion.setAngles("LShoulderPitch", .4, pctMax)
    motion.setAngles("RShoulderPitch", .4, pctMax)
    time.sleep(.5)

    motion.setAngles("LArm", realStart, .2)
    motion.setAngles("RArm", holderPlacement, .2)
    time.sleep(1)

def toRestPosition():
    motion.setAngles("LShoulderRoll", 1.25, .1)
    motion.setAngles("RShoulderRoll", -1.25, .1)
    time.sleep(1)

    motion.setAngles("LElbowRoll", 0, pctMax)
    motion.setAngles("RElbowRoll", 0, pctMax)
    time.sleep(1)

    motion.setAngles("LShoulderPitch", 1.5, pctMax)
    motion.setAngles("RShoulderPitch", 1.5, pctMax)
    time.sleep(1)

    motion.setAngles("LShoulderRoll", .2, pctMax)
    motion.setAngles("RShoulderRoll", -.2, pctMax)
    time.sleep(1)

    motion.rest()

# Draw a card from the top of the stack into Ace's left hand.
T_CH = None
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
    outerPos = centerCardR[:]
    # Adjust shoulder to be further out to the side
    outerPos[1] = -60 * d2r
    outerPos[-1] = 1 # open hand

    # put right hand to the right of the card, so we can move the hand in without colliding with the card
    motion.setAngles("RArm", outerPos, pctMax)
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
    ids, xs, Rs = ComputerVision.getVisibleCards()
    checkDrawnCard = ComputerVision.getDrawnCard(ids, xs, Rs)



# Assuming a card is in Ace's right hand, hand it off to the left hand
def handOffRtoL():
    # Move the left hand to center the card in front of Ace's chest
    motion.setAngles("RArm", centerCardR, pctMax)
    time.sleep(1.5)

    # Make a copy of the left arm pose
    outerPos = centerCardL[:]
    # Adjust shoulder to be further out to the side
    outerPos[1] = 60 * d2r
    outerPos[-1] = 1

    # put right hand to the right of the card, so we can move the hand in without colliding with the card
    motion.setAngles("LArm", outerPos, pctMax)
    time.sleep(1.5)

    # move the left hand in, so it can grab the card.
    motion.setAngles("LShoulderRoll", centerCardL[1], pctMax)
    time.sleep(1)

    # Loosen right hand grip so left hand can "pull it out" as it grabs the card.
    motion.setStiffnesses("RHand", .5)

    # Grab the card with the left hand
    motion.setAngles("LHand", .27, pctMax)
    time.sleep(.5)

    # Release with the right hand
    motion.setAngles("RHand", 1, pctMax)
    time.sleep(.5)

    # Move left arm out of the way, and restore the hand's stiffness
    motion.setAngles("RShoulderRoll", -60 * d2r, pctMax)
    motion.setStiffnesses("RHand", 1)
    time.sleep(1)

    #TODO check card again; other corner should be visible now
    drawnCard = None
    absLayer.drewCard.trigger(drawnCard)

# Assuming the card is in Ace's right hand, put it into the tray at in the [offset]th position
def placeCardInHolder(offset):
    targetPos = holderPlacement[:]

    targetPos[1] -= 10 * d2r * offset

    startPos = [ targetPos[i] + trayPlaceOffset[i] for i in range(len(targetPos)) ]

    motion.setAngles("RArm", startPos, pctMax)
    time.sleep(1)

    motion.setAngles("RArm", targetPos, pctMax)
    time.sleep(.5)

    motion.setAngles("RHand", 1, pctMax)
    time.sleep(.5)

# these are random guesses, fix before running
slot0 = [.5, -.15, -.06, 0, 0, 0]
def testPerfectPositioning(offset):
    targetPosition = slot0[:]
    targetPosition[1] -= .025 * offset
    targetPosition[0] -= .03

    motion.setPositions("RArm", 0, targetPosition, pctMax, 63 - 16) # axis mask = all axes except y axis (pitch)
    time.sleep(1)

    targetPosition[0] += .03
    motion.setPositions("RArm", 0, targetPosition, pctMax, 63 - 16)
    time.sleep(1)

    motion.setAngles("RHand", 1, pctMax)
    time.sleep(.5)

def testCardRelative(offset):
    targetPosition = slot0[:]
    targetPosition[1] -= .025 * offset

    targetTf = almath.Transform_fromPosition(*targetPosition)
    # T_CT

    # T_HT = T_CT * T_CH^-1
    target_HT = np.matmul( targetTf, np.linalg.inv( T_CH ) )

    targetHandPos = almath.position6DFromTransform( target_HT )

    motion.setPositions("RArm", 0, targetHandPos, pctMax, 63)
    time.sleep(1)

    motion.setAngles("RHand", 1, pctMax)
    time.sleep(.5)


    
# use Ace's right hand to pick up the card in the [offset]th slot of Ace's hand
def pickUpFromHolder(offset):
    targetPos = holderPlacement[:]
    targetPos[1] -= 10 * d2r * offset
    targetPos[-1] = 1 # open hand

    # move arm above the target card
    motion.setAngles("RArm", targetPos, pctMax)
    time.sleep(1)

    # move arm down to put hand around card
    motion.changeAngles("RShoulderPitch", 10*d2r, pctMax)
    time.sleep(.5)

    motion.setAngles("RHand", .28, pctMax)
    time.sleep(.5)

    # move arm back up to pull out card
    motion.changeAngles("RShoulderPitch", -40*d2r, pctMax)
    time.sleep(1)

    # turn wrist around to get card completely clear from tray
    #motion.setAngles("RWristYaw", )

# TODO implement
# assuming a card is in Ace's left hand, place it on the discard pile
def playCard():
    pass

def onDrawCard():
    drawCard()
    handOffLtoR()
    # we can't put the card into the tray yet, we wait for the drewCard Event
    # to know what we drew to update the hand and know where to put the card.

# once we know which card we drew, find a slot for it in the hand and put it there
def onDrewCard(card):
    # type: (AbstractionLayer.Card)->None
    # scan for an empty slot, put the card there if we find one.
    for offset in range(len(hand)):
        if hand[offset] == None:
            hand[offset] = card
            break
    # if we don't find an empty slot, add one to the end
    if(hand[offset] != None):
        offset = len(hand)
        hand.append(card)
    
    placeCardInHolder(offset)

def onPlayCard(cardToPlay, suitStringForEights):
    #type: (AbstractionLayer.Card)->None
    for offset, cardInHand in enumerate(hand):
        if(cardInHand == cardToPlay):
            cardInHand = None
            break
    # we couldn't find the card we want to play in our hand
    else:
        # TODO panic
        pass

    pickUpFromHolder(offset)
    handOffRtoL()
    playCard()
    absLayer.playedCard.trigger()



# Set up abstraction layer callbacks

absLayer.drawCard.subscribe(onDrawCard)
absLayer.drewCard.subscribe(onDrewCard)
absLayer.playCard.subscribe(onPlayCard)
