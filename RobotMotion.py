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
Edited 2/8/2024
  - Added and refined calibration routine
Revised 2-19-2024 (Shelby Jones)
    - removed tts calls, replaced with absLayer triggers
Edited 2/20/2024
  - Adjusted calibration animations, added vision for tray animations
Edited 2/26/2024 (Elise Lovell)
  - added skeletal turnHead functions
Edited 2/28/2024 (Elise Lovell)
   - finished turnHead with appropriate funciton calls
Edited 3/18/2024 (Elise Lovell)
  - added lookForward() and abstraction subscribe
Edited 3/22/2024 (Liam McKinney)
  - adjusted various animations for consistency
Edited 4/3/2024 (Liam McKinney)
  - removed l2rJoints and changed all positions to left-arm angles
Edited 4/13/2024 (Elise Lovell)
   - added blackjack functions
"""
import time
from naoqi import ALProxy
import RobotInfo
import AbstractionLayer
import numpy as np
import almath
import hand
import ComputerVision
from Card import Card
import threading

absLayer = AbstractionLayer.AbstractionLayer()

d2r = 3.14159 / 180

# percent of max speed to be used for most animations
pctMax = .35

motion = ALProxy("ALMotion", RobotInfo.getRobotIP(), RobotInfo.getPort())
temp = ALProxy("ALBodyTemperature", RobotInfo.getRobotIP(), RobotInfo.getPort())

# predefined positions for drawing/playing Cards

# Joint order: ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand']
realStart = [0.1548919677734375, -0.1, -90 * d2r, -0.03490658476948738, 90 * d2r, .65]


helpComplete = threading.Event()
helpComplete.set()
# We need to track if we were moving a card when we asked for help, so we can mention it when describing our hand.
wasMovingCard = False

def wakeRobot():
    motion.wakeUp()
    readyArms()

def readyArms():
    motion.setAngles("LShoulderRoll", 1.25, pctMax)
    time.sleep(.5)

    motion.setAngles("LShoulderPitch", .4, pctMax)
    time.sleep(.5)

    motion.setAngles("LArm", realStart, .2)
    time.sleep(1)

def toRestPosition():
    motion.setAngles("LShoulderRoll", 1.25, .1)
    time.sleep(1)

    motion.setAngles("LElbowRoll", 0, pctMax)
    time.sleep(1)

    motion.setAngles("LShoulderPitch", 1.5, pctMax)
    time.sleep(1)

    motion.setAngles("LShoulderRoll", .2, pctMax)
    time.sleep(1)

    motion.rest()

# Draw a card from the top of the stack into Ace's left hand.
T_CH = None
def drawCard():
    # starting position
    motion.angleInterpolationWithSpeed("LArm", realStart, pctMax)

    # Allow the elbow to bend freely so we can easily "drag" the hand along the deck
    motion.setStiffnesses("LElbowRoll", 0)
    # slowly lower the shoulder to drag the hand along the top of the deck, separating the top card
    motion.changeAngles("LShoulderPitch", 40 * d2r, .1)
    time.sleep(1.5)

    motion.setStiffnesses("LElbowRoll", 1)
    time.sleep(.5)

    motion.changeAngles("LElbowRoll", -10*d2r, pctMax)
    time.sleep(.5)

    # grab the card
    motion.setAngles("LHand", .25, pctMax)
    time.sleep(1)

    # pull the card the rest of the way out
    motion.changeAngles("LElbowRoll", -20 * d2r, .2)
    time.sleep(1)

    motion.changeAngles("LShoulderPitch", -20 * d2r, pctMax)
    time.sleep(1)

    # Straighten out elbow and rotate joints to make a smoother transition to the hand tray animations
    motion.changeAngles("LShoulderPitch", -40*d2r, pctMax)
    motion.setAngles("LElbowRoll", 0, pctMax)
    motion.setAngles("LElbowYaw", 90 * d2r, pctMax)
    motion.setAngles("LWristYaw", -90 * d2r, pctMax)
    time.sleep(1)

    motion.changeAngles("LShoulderPitch", -60 * d2r, pctMax)
    motion.changeAngles("LElbowRoll", -120*d2r, pctMax)
    time.sleep(1)


# Position where the bot grabs cards from the left or right stack
lStackPos = [0.1548919677734375, 0.705974278834025, 1.370795, -0.03490658476948738, -1.570795, 1]#[0.1548919677734375, -0.7583341121673584, 0.2, 0.03490658476948738, 0, 1]
rStackPos = [0.10253213444010417, 0.3, 1.370795, -0.03490658476948738, -1.570795, 1]
#rStackPos = [0.10253213444010417, -0.37981154785325794, -1.370795, 0.03490658476948738, 1.570795, 1]#[0.1548919677734375, -0.41471810340881348, 0.2, 0.03490658476948738, 0, 1]

lPlayStart = [-0.7256240844726562, 0.49697399139404297, 2.023303985595703, -1.0783600807189941, -1.5938677787780762, 0.25]
rPlayStart = [-0.5476799011230469, 0.21011614799499512, 1.8729721307754517, -1.0660879611968994, -1.8116960525512695, 0.25]

# Used to specify which stack to play/pick up from
L = True
R = False

lCards = []
rCards = []

# Put a card from the bot's hand onto the specified stack
def playOnStack(side):
    arm = "LArm"
    shoulder = "LShoulderPitch"

    if side == L:
        targetPos = lStackPos[:]
        wristTwist = 10*d2r
    else:
        targetPos = rStackPos[:]
        wristTwist = 0

    # Keep hand closed, raise shoulder to put hand above the cards
    targetPos[-1] = .25

    pitchUp = (30 if side==L else 20) * d2r
    targetPos[0] -= pitchUp

    # Adjust elbow/wrist angles so elbow faces down (keeps card straight on to the stack)
    targetPos[-4] -= (-15 if side==L else -10) * d2r
    targetPos[-2] += wristTwist

    startPos = lPlayStart[:] if side == L else rPlayStart[:]
    startPos[-1] = .25

    # Pull back the end position slightly so we don't overshoot the holder
    targetPos[0] -= 10 * d2r
    targetPos[-3] -= 20 * d2r

    motion.angleInterpolationWithSpeed(arm, startPos, .2)
    motion.angleInterpolationWithSpeed(arm, targetPos, pctMax)
    motion.setAngles("LHand", .3, pctMax)
    time.sleep(.5)
    motion.changeAngles(shoulder, pitchUp * .75, pctMax)
    time.sleep(.5)
    motion.setAngles("LHand", 1, pctMax)
    time.sleep(.5)
    motion.changeAngles(shoulder, -pitchUp * .75, pctMax)
    time.sleep(.5)
    motion.changeAngles("LShoulderRoll", 20*d2r, pctMax)
    motion.setAngles("HeadYaw", 45*d2r, pctMax)
    time.sleep(.5)

    # We figure out what card we're putting on the stack after the animation is over
    # because we may not know what card we're holding (e.g. after drawing a card)
    cards = lCards if side == L else rCards

    drawnCard = None

    # Make sure we have a new card in the tray. If not, ask for help until we do.
    while drawnCard == None or drawnCard in cards:
        topCard = ComputerVision.getStackTop(side)
        if topCard == None:
            # No card in tray means Nao failed to put the card in the tray,
            # possibly knocking over others as well. Nao must ask for help.
            absLayer.SayWords.trigger("Oops, I must have dropped something. Could someone fix my cards for me?")
            waitForHelp(True)
            continue
        
        drawnCard = Card(str(topCard[0]), str(topCard[1]))
        if drawnCard in cards:
            # If the top card is one that was already in the stack, we messed something up. Ask for help.
            absLayer.SayWords.trigger("Oops, I must have dropped something. Could someone fix my cards for me?")
            waitForHelp(True)
            continue

    cards.append(drawnCard)

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
        wristTwist = 10 * d2r
    else:
        targetPos = rStackPos[:]
        pullBackPos = rPlayStart[:]
        wristTwist = 0

    # Put hand above the holder so we don't wipe out the cards on our way to the pick up position.

    targetPos[-1] = 1
    startPos = targetPos[:]

    startPos[0] -= 30 * d2r
    startPos[-3] -= 15 * d2r

    pullBackPos[0] -= 20 * d2r
    pullBackPos[-1] = .3

    motion.angleInterpolationWithSpeed(arm, startPos, pctMax)
    # Move arm down to put hand around cards
    motion.angleInterpolationWithSpeed(arm, targetPos, pctMax)
    # Lightly press against the front of the cards
    motion.setStiffnesses(hand, .3)
    motion.setAngles(hand, .4, pctMax)
    time.sleep(1.5)
    # Raise hand upwards, dragging the top card with it
    pitchUp = -20*d2r if side==L else -15*d2r
    motion.changeAngles(shoulder, pitchUp, .1)
    motion.changeAngles("LWristYaw", wristTwist, .1)
    time.sleep(.5)
    # Grab the top card the rest of the way, now that the stack is out of the way
    motion.setStiffnesses(hand, 1)
    #motion.setAngles(hand, .29, pctMax)
    #time.sleep(.5)

    # Pull arm back by simultaneously bending the elbow and moving the shoulder out.
    # This prevents us from dragging the other cards left or right on the tray.
    motion.angleInterpolationWithSpeed("LHand", .25, pctMax)
    motion.angleInterpolationWithSpeed(arm, pullBackPos, pctMax)
    
    time.sleep(1)

# assuming a card is in Ace's left hand, place it on the discard pile
def playCard():
    targetPos = realStart[:]
    targetPos[1] -= 15 * d2r
    targetPos[2] += 20 * d2r
    targetPos[-3] -= 20 * d2r
    targetPos[-2] = -90 * d2r
    targetPos[-1] = .25

    motion.angleInterpolationWithSpeed("LArm", targetPos, pctMax)
    #motion.setStiffnesses("LElbowRoll", 0)
    motion.changeAngles("LShoulderPitch", 25*d2r, pctMax)
    time.sleep(1)
    motion.setAngles("LHand", 1, pctMax)
    time.sleep(.5)
    motion.setAngles("LHand", 0, pctMax)
    time.sleep(.5)
    #motion.setStiffnesses("LElbowRoll", 1)
    motion.changeAngles("LShoulderPitch", -20*d2r, pctMax)
    time.sleep(.5)

    endPos = realStart[:]
    endPos[0] -= 20*d2r
    motion.angleInterpolationWithSpeed("LArm", endPos, pctMax)

#draw card crazy 8
def onDrawCard():
    drawCard()
    playOnStack(R)

    absLayer.drewCard.trigger(rCards[-1])
    # we can't put the card into the tray yet, we wait for the drewCard Event
    # to know what we drew to update the hand and know where to put the card.

#draw card Blackjack
def drawBlackJack():
    drawCard()
    playOnStack(R)

    absLayer.hitReturn.trigger(rCards[-1])
    # we can't put the card into the tray yet, we wait for the drewCard Event
    # to know what we drew to update the hand and know where to put the card.

def onPlayCard(cardToPlay, _):
    #type: (AbstractionLayer.Card, str)->None
    #search for card

    if cardToPlay in lCards:
        inLStack = True
    elif cardToPlay in rCards:
        inLStack = False
    else:
        # We don't have the card we need. Something went wrong, we need help.
        absLayer.SayWords.trigger("Oops. I seem to have lost the %s. Could someone find it and play it for me?")
        waitForHelp(False)

        # The user already played the card for us, no need to do anything else.
        absLayer.playedCard.trigger()
        return


    fromStack = L if inLStack else R
    toStack = R if inLStack else L
    cards = lCards if inLStack else rCards

    while len(cards) > 0 and cards[-1] != cardToPlay:
        pickupFromStack(fromStack)
        playOnStack(toStack)
        cards = lCards if inLStack else rCards

    if len(cards) == 0:
        #panic
        return

    pickupFromStack(fromStack)
    playCard()

    absLayer.playedCard.trigger()

#draw five cards on the start of the game
def startingHand():
  arr = []
  #loop to draw five cards
  for x in range(5):
    #draw card
    drawCard()
    playOnStack(R)
    #add new card to array
    arr.append(rCards[-1])
  #give abs layer list of cards drawn
  absLayer.returnSH.trigger(arr)

#draw two starting cards for blackjack
def startingHandBlackJack():
  arr = []
  #loop to draw five cards
  for x in range(2):
    #draw card
    drawCard()
    playOnStack(R)
    #add new card to array
    arr.append(rCards[-1])
  #give abs layer list of cards drawn
  absLayer.startBlackJack.trigger(arr)

calibStep = 0
calibInstructions = [
    "Place a card tray under my hand, against my thumb",
    "Place a card tray under my hand, against my thumb",
    "Place the deck holder against my fingers"
]
intermedPositions = [
    [lStackPos],
    [lStackPos, rStackPos],
    [rStackPos, realStart[:]]
]
calibPositions = [
    lStackPos,
    rStackPos,
    [1.1090400218963623, -0.09668397903442383, -1.659830093383789, -0.9418339729309082, -1.5355758666992188, 0.9847999811172485]
]
def onStartCalibration():
    # Populate calibPositions with correct poses based on l/rStackPos
    calibPositions[0] = lStackPos[:]
    calibPositions[0][0] -= 5*d2r
    calibPositions[0][-1] = .8

    intermedPositions[0][0] = lStackPos[:]
    intermedPositions[0][0][0] -= 15*d2r

    calibPositions[1] = rStackPos[:]
    calibPositions[1][0] -= 5*d2r
    calibPositions[1][-1] = .8

    intermedPositions[1][0] = lStackPos[:]
    intermedPositions[1][0][0] -= 25*d2r

    intermedPositions[1][1] = rStackPos[:]
    intermedPositions[1][1][0] -= 25*d2r

    intermedPositions[2][0] = rStackPos[:]
    intermedPositions[2][0][0] -= 25*d2r

    intermedPositions[2][1] = realStart[:]
    intermedPositions[2][1][0] -= 25*d2r
    intermedPositions[2][1][-2] = -90*d2r

    global calibStep
    calibStep = 0
    onNextCalibStep()

def onNextCalibStep():
    global calibStep
    if calibStep >= len(calibPositions):
        absLayer.SayWords.trigger("Calibration Complete.")
        finishCalibration()
        return
    for posn in intermedPositions[calibStep]:
        motion.angleInterpolationWithSpeed("LArm", posn, pctMax)
    motion.setAngles("LArm", calibPositions[calibStep], pctMax)
    absLayer.SayWords.trigger(calibInstructions[calibStep])
    calibStep += 1

#Move nao's arm from final calibration step to the initial draw position without disrupting the deck
def finishCalibration():
    motion.setStiffnesses("LElbowRoll", 0)
    time.sleep(.5)
    motion.changeAngles("LShoulderPitch", 8*d2r, pctMax)
    time.sleep(.5)
    motion.setAngles("LHand", 0, pctMax)
    motion.setStiffnesses("LElbowRoll", 1)
    time.sleep(.5)
    motion.changeAngles("LShoulderPitch", -50*d2r, pctMax)
    time.sleep(1)

    motion.angleInterpolationWithSpeed("LArm", realStart, pctMax)

def turnHeadMove(currPlayer, totalPlayers):
  #total players includes Nao
  if currPlayer != 0:
    #turn (180/totalPlayers) * currPlayers
    #0 = straight infront
    #+ is to the left, - to the right
    degreeSegments = 180/totalPlayers
    currPlayerAngle = 90- (degreeSegments * currPlayer)
    motion.angleInterpolationWithSpeed("HeadYaw", currPlayerAngle*d2r,pctMax)

def turnHeadForward():
    motion.angleInterpolationWithSpeed("HeadYaw", 0, pctMax)

# Blocks until the user says they have finished helping.
# Will then return normally and allow the caller to continue execution.
# Because each command works on a different thread, we are fine to stall execution like this,
# as long as we make sure the speech recognition doesn't stay paused.
def waitForHelp(fromMovingCard):
    global wasMovingCard
    wasMovingCard = fromMovingCard

    absLayer.awaitHelp.trigger()

    helpComplete.clear()
    helpComplete.wait()

# If the robot needs help fixing its hand, we are willing to tell the user the contents of Nao's hand if necessary.
def onHandRequest():
    if not helpComplete.is_set():
        handString = ""
        for (traySide, cards) in [("left", lCards), ("right", rCards)]:
            if len(cards) == 0:
                print("empty case")
                handString += "My %s tray should be empty. " % traySide
            elif len(cards) == 1:
                print("single case")
                handString += "My %s tray should only have the %s." % (traySide, cards[0].cardName())
            else:
                print("multi case")
                handString += "The cards in my %s tray, from bottom to top, should be " % traySide
                for card in cards[:-1]:
                    handString += "the %s, " % card.cardName()
                handString += "and the %s. " % cards[-1].cardName()

        if(wasMovingCard):
            handString += "The card I was just trying to move should be at the top of the stack in my right tray."

        absLayer.SayWords.trigger(handString)

# User says they are finished helping, we can resume execution
def onHelpReceived():
    helpComplete.set()

# Set up abstraction layer callbacks

# Set up abstraction layer callbacks
absLayer.turnHead.subscribe(turnHeadMove)
absLayer.faceForward.subscribe(turnHeadForward)

absLayer.drawBlackJackStart.subscribe(startingHandBlackJack)
absLayer.drawStartingHand.subscribe(startingHand)
absLayer.drawCard.subscribe(onDrawCard)
absLayer.hit.subscribe(drawBlackJack)
absLayer.playCard.subscribe(onPlayCard)

absLayer.startCalib.subscribe(onStartCalibration)
absLayer.nextCalibStep.subscribe(onNextCalibStep)

absLayer.handRequested.subscribe(onHandRequest)
absLayer.helpComplete.subscribe(onHelpReceived)