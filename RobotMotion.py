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
Edited 12/2/2023
  - Added function for drawing starting hand - Elise Lovell
Edited 12/3/2023
  - Added basic animations for 2-stack hand management
Edited 1/28/2024
  - Refined 2-stack hand, added virtual hand arrays, implemented play motion
"""
import time
from naoqi import ALProxy
import RobotInfo
import AbstractionLayer
import numpy as np
import almath
#from positioning.Pose import *
#import ComputerVision

# translate a 3d point or Position6D to work with the other arm
def l2rPosn(vec):
    if len(vec) == 3:
        return [vec[0], -vec[1], vec[2]]
    else:
        return [vec[0], -vec[1], vec[2], -vec[3], vec[4], -vec[5]]

# translate joint positions to give the same (mirrored) position with the other arm
def l2rJoints(vec):
    return [vec[0], -vec[1], -vec[2], -vec[3], -vec[4], vec[5]]

absLayer = AbstractionLayer.AbstractionLayer()

d2r = 3.14159 / 180

# percent of max speed to be used for most animations
pctMax = .35

motion = ALProxy("ALMotion", RobotInfo.getRobotIP(), RobotInfo.getPort())
temp = ALProxy("ALBodyTemperature", RobotInfo.getRobotIP(), RobotInfo.getPort())

# predefined positions for drawing/playing Cards

# Joint order: ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand']
realStart = [0.1548919677734375, -0.07060599327087402, -90 * d2r, -0.03490658476948738, 90 * d2r, .65]

holderPlacement = [-0.0827939, -0.25622, 0.246933, 0.325249, -0.246933, 0.27]

# offset to the holderPlacement position to "pull back" the card slightly
trayPlaceOffset = [0, -30*d2r, 0, 60*d2r, 0, 0]

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
    motion.angleInterpolationWithSpeed("LArm", realStart, pctMax)
    time.sleep(.5)

    # Allow the elbow to bend freely so we can easily "drag" the hand along the deck
    motion.setStiffnesses("LElbowRoll", 0)
    # slowly lower the shoulder to drag the hand along the top of the deck, separating the top card
    motion.changeAngles("LShoulderPitch", 40 * d2r, .1)
    time.sleep(1.5)

    motion.setStiffnesses("LElbowRoll", 1)
    time.sleep(.5)
    # Lift the elbow slightly to get the hand in better grabbing position
    #motion.changeAngles("LElbowRoll", -15 * d2r, .1)
    #time.sleep(1)

    # Move the hand forward to position the thumb under the card so it can grab
    #motion.changePosition("LArm", 0, [.01, 0, 0, 0, 0, 0], pctMax, 7)
    #time.sleep(1)

    # grab the card
    motion.setAngles("LHand", .4, pctMax)
    time.sleep(1)

    # pull the card the rest of the way out
    motion.changeAngles("LElbowRoll", -20 * d2r, pctMax)
    time.sleep(1)

    motion.changeAngles("LShoulderPitch", -20 * d2r, pctMax)
    time.sleep(1)

    # Rotate the hand 180 degrees to remove the card from the tray completely
    motion.setAngles("LWristYaw", -100 * d2r, pctMax)
    time.sleep(1)

    # Straighten out elbow and rotate joints to make a smoother transition to the hand tray animations
    motion.changeAngles("LShoulderPitch", -40*d2r, pctMax)
    motion.setAngles("LElbowRoll", 0, pctMax)
    motion.setAngles("LElbowYaw", 90 * d2r, pctMax)
    motion.setAngles("LWristYaw", -90 * d2r, pctMax)
    time.sleep(1)

# Assuming a card is in Ace's left hand, hand it off to the right hand
def handOffLtoR():
    # Move the left hand to center the card in front of Ace's chest
    motion.setAngles("LArm", centerCardL, pctMax)
    time.sleep(1.5)

    # Check what card we drew, if we can see the marker
    #ids, xs, Rs = ComputerVision.getVisibleCards()
    #drawnCard = ComputerVision.getDrawnCard(ids, xs, Rs)

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
    #ids, xs, Rs = ComputerVision.getVisibleCards()
    #checkDrawnCard = ComputerVision.getDrawnCard(ids, xs, Rs)



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
    arm = "LArm"
    hand = "LHand"

    targetPos = holderPlacement[:]

    targetPos[1] -= 10 * d2r * offset

    startPos = [ targetPos[i] + trayPlaceOffset[i] for i in range(len(targetPos)) ]

    motion.setAngles(arm, l2rJoints(startPos), pctMax)
    time.sleep(1)

    motion.setAngles(arm, l2rJoints(targetPos), pctMax)
    time.sleep(.5)

    motion.setAngles(hand, 1, pctMax)
    time.sleep(.5)

# Position where the bot grabs cards from the left or right stack
lStackPos = [0.1548919677734375, -0.705974278834025, -1.370795, 0.03490658476948738, 1.570795, 1]#[0.1548919677734375, -0.7583341121673584, 0.2, 0.03490658476948738, 0, 1]
rStackPos = [0.10253213444010417, -0.37981154785325794, -1.370795, 0.03490658476948738, 1.570795, 1]#[0.1548919677734375, -0.41471810340881348, 0.2, 0.03490658476948738, 0, 1]

lPlayStart = [-0.7256240844726562, -0.49697399139404297, -2.023303985595703, 1.0783600807189941, 1.5938677787780762, 0.25]
rPlayStart = [-0.5476799011230469, -0.21011614799499512, -1.8729721307754517, 1.0660879611968994, 1.8116960525512695, 0.25]

#These are for the left arm, MAKE SURE you use coordinates for the correct arm
lposn6d = [0.1564960479736328, 0.24610111117362976, 0.06121184676885605, -0.13601450622081757, 0.15259084105491638, 0.6932932138442993]
rposn6d = [0.19680142402648926, 0.18685270845890045, 0.06395590305328369, -0.18415850400924683, 0.1372106373310089, 0.3608408272266388]
# Used to specify which stack to play/pick up from
L = True
R = False

# Hand joint position to press thumb against the cards
medHand = .5

lCards = []
rCards = []

# Put a card from the bot's hand onto the specified stack
def playOnStack(side):
    arm = "LArm"
    hand = "LHand"
    shoulder = "LShoulderPitch"

    if(side == L):
        targetPos = lStackPos[:]
    else:
        targetPos = rStackPos[:]

    # Keep hand closed, raise shoulder to put hand above the cards
    targetPos[-1] = .4

    pitchUp = (25 if side==L else 20) * d2r
    targetPos[0] -= pitchUp

    # Adjust elbow/wrist angles so elbow faces down (keeps card straight on to the stack)
    targetPos[-4] += (-15 if side==L else -10) * d2r
    #targetPos[-2] += 90 * d2r
    #targetPos[1] += .1

    startPos = lPlayStart[:] if side == L else rPlayStart[:]
    startPos[-1] = .4

    # Pull back the end position slightly so we don't overshoot the holder
    targetPos[0] -= 10 * d2r
    targetPos[-3] += 20 * d2r

    motion.angleInterpolationWithSpeed(arm, l2rJoints(startPos), pctMax)
    time.sleep(.5)
    motion.angleInterpolation(arm, l2rJoints(targetPos), .5, True)
    time.sleep(.5)
    motion.changeAngles(shoulder, pitchUp, pctMax)
    time.sleep(.5)
    motion.setAngles(hand, 1, pctMax)
    time.sleep(.5)
    motion.changeAngles(shoulder, -pitchUp, pctMax)
    time.sleep(.5)
    #motion.changeAngles(shoulder, 20 * d2r, pctMax)
    #time.sleep(.5)
    #motion.setAngles(hand, 1, pctMax)

    # We figure out what card we're putting on the stack after the animation is over
    # because we may not know what card we're holding (e.g. after drawing a card)
    topCard = None #TODO use ComputerVision to identify top card
    cards = lCards if side == L else rCards
    cards.append(topCard)

# Pick up the top card of the specified stack 
def pickupFromStack(side):
    arm = "LArm"
    hand = "LHand"
    shoulder = "LShoulderPitch"

    cards = lCards if side == L else rCards
    cards.pop()

    if side == L:
        targetPos = lStackPos[:]
        pullBackPos = lPlayStart[:]
    else:
        targetPos = rStackPos[:]
        pullBackPos = rPlayStart[:]

    # Put hand above the holder so we don't wipe out the cards on our way to the pick up position.
    targetPos[0] -= 30 * d2r
    targetPos[-1] = 1

    pullBackPos[0] -= 20 * d2r
    pullBackPos[-1] = .4

    motion.setAngles(arm, l2rJoints(targetPos), pctMax)
    time.sleep(1)
    # Move arm down to put hand around cards
    motion.changeAngles(shoulder, 33 * d2r, pctMax)
    time.sleep(.5)
    # Lightly press against the front of the cards
    motion.setStiffnesses(hand, .2)
    motion.setAngles(hand, medHand, pctMax)
    time.sleep(1.5)
    # Raise hand upwards, dragging the top card with it
    motion.changeAngles(shoulder, -20 * d2r, pctMax)
    time.sleep(.5)
    # Grab the top card the rest of the way, now that the stack is out of the way
    motion.setStiffnesses(hand, 1)
    #motion.setAngles(hand, .29, pctMax)
    #time.sleep(.5)

    # Pull arm back by simultaneously bending the elbow and moving the shoulder out.
    # This prevents us from dragging the other cards left or right on the tray.
    motion.angleInterpolationWithSpeed("LArm", l2rJoints(pullBackPos), pctMax)
    #offset = [-.03, .01, .02, 0, 0, 0]
    #posn = l2rPosn(motion.getPosition(arm, 0, True))
    #tgt = [posn[i] + offset[i] for i in range(6)]
    #motion.positionInterpolations("LArm", 0, l2rPosn(tgt), 7, .5)
    time.sleep(.5)

def playFromLStack():
    pickupFromStack(L)
    playCard()

def moveLtoR():
    pickupFromStack(L)
    playOnStack(R)

def moveRtoL():
    pickupFromStack(R)
    playOnStack(L)
    
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
    targetPos = realStart[:]
    targetPos[1] += 10 * d2r
    targetPos[-2] = -90 * d2r

    motion.setAngles("LArm", targetPos, pctMax)
    time.sleep(1)
    motion.changeAngles("LShoulderPitch", 20*d2r, pctMax)
    time.sleep(1)
    motion.setAngles("LHand", 1, pctMax)
    time.sleep(.5)
    motion.changeAngles("LShoulderPitch", -20*d2r, pctMax)
    time.sleep(.5)

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

def onPlayCard(cardToPlay, _):
    #type: (AbstractionLayer.Card, str)->None
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

#draw five cards on the start of the game
def startingHand():
  arr = []
  #loop to draw five cards
  for x in range(6):
    #draw card
    drawCard()
    #recognize and turn into card object
    values = []
    #commented out for pythoc 3 usability
    #values = ComputerVision.getDrawnCard(ComputerVision.getVisibleCards())
    v = "" + values[0]
    s = "" + values[1]
    c = hand.Card(v, s)
    #add new card to array
    arr.push(c)
    #put card in holder
    handOffLtoR()
  #give abs layer list of cards drawn
  absLayer.returnSH.trigger(arr)
    
    

# Set up abstraction layer callbacks

absLayer.drawStartingHand.subscribe(startingHand)
absLayer.drawCard.subscribe(onDrawCard)
absLayer.drewCard.subscribe(onDrewCard)
absLayer.playCard.subscribe(onPlayCard)
