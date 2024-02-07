"""
CommandDetection.py
Handles the Nao's detection of commands by human opponents
Created by Liam McKinney
Created 10/2/2023
Revised 10/19/2023
    -testing command detection(Liam McKinney)
Revised 12/1/2023
    -Added Detection for player ending their turn (Shelby Jones)
Revised 12/2/2023
    -revised for clarity (Elise Lovell)
Revised 12-4-2023
    -revised logical errors in calling the end of players turn (Shelby Jones)
Revised 01/24/2024
    -Added commands to recognize and act upon players winning or shuffling the deck (Nathan Smith)
Revised 1/24/2024
     - added hearNumPlayers() function and connected to absLayer (Elise Lovell)
Revised 1/24/2024
     - added phrases to command library (Elise Lovell)
Revised 1/31/2024
     - added game_state variable, which locks certain functions based on innappropriate game states (Nathan Smith)
"""


from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker
import RobotInfo
import atexit
import FSM
import AbstractionLayer
import ComputerVision
import random

EVENT_NAME = "WordRecognized"
MODULE_NAME = "CommandDetector"
absLayer = AbstractionLayer.AbstractionLayer()
# Global variable to store the CommandDetector module instance
CommandDetector = None
memory = None

#Global variable to track the gamestate for command activation purposes
game_state = "pregame"
tts = None

def init():
    global CommandDetector

    # the only thing we need this module for is to disable a "listening animation"
    moves = ALProxy("ALAutonomousMoves", RobotInfo.getRobotIP(), RobotInfo.getPort())
    moves.setExpressiveListeningEnabled(False)

    commands = { #WHAT THE ROBOT IS LISTENING FOR

        #commands to start a game
        "Start game": hearStartGame, 
        "Let's start a game": hearStartGame,

        #commands to end a player's turn
        "I end my turn": endTurnOpp,
        "end turn": endTurnOpp,
        "my turn is over": endTurnOpp,
        "end": endTurnOpp, 
        "over": endTurnOpp,
        "done": endTurnOpp,
        #commands to announce a player has won
        "I win": playerWins,
        "I have won": playerWins, 
        "We Win": playerWins,
        "I am victorious!": playerWins,
        #commands to announce the deck is being shuffled
        "I will now shuffle the deck": deckShuffle,
        "I am going to shuffle the deck": deckShuffle,
        "Shuffling": deckShuffle,
        #commands for number of people playing the game
        "1 player": hearNumPlayers,
        "2 players": hearNumPlayers,
        "3 players": hearNumPlayers, 
        "4 players": hearNumPlayers, 
        "5 players": hearNumPlayers,
        "6 players": hearNumPlayers,

        #commands to start/continue the board setup/calibration process
        "Begin calibration": startCalib,
        "Next step": continueCalib
        }

    CommandDetector = CommandDetectorModule(MODULE_NAME, commands)
def deinit():
    memory.unsubscribeToEvent(EVENT_NAME, MODULE_NAME)
    CommandDetector.asr.unsubscribe(MODULE_NAME)
class CommandDetectorModule(ALModule):
    """ A simple module able to react
    to voice commands
    """
    def __init__(self, name, commands):
        ALModule.__init__(self, name)
        self.commands = commands
        # Create proxies for speech recognition and text to speech (for debugging)
        self.asr = ALProxy("ALSpeechRecognition", RobotInfo.getRobotIP(), RobotInfo.getPort())

        self.tts = ALProxy("ALTextToSpeech", RobotInfo.getRobotIP(), RobotInfo.getPort())

        # set list of recognized commands
        self.asr.setVocabulary(commands.keys(), False)

        # get nao to start writing recognized phrases in ALMemory
        self.asr.subscribe(MODULE_NAME)
        # Subscribe to the WordRecognized event:
        global memory
        memory = ALProxy("ALMemory", RobotInfo.getRobotIP(), RobotInfo.getPort())
        memory.subscribeToEvent(EVENT_NAME,
            MODULE_NAME,
            "onWordRecognized")
    def onWordRecognized(self, key, value, message):
        """ This will be called each time a command is
        detected.
        """
        # Pause speech recognition while performing commands
        self.asr.pause(True)
        #memory.unsubscribeToEvent(EVENT_NAME,
        #    MODULE_NAME)
        print(value)
        #if confidence is high enough, run the command
        if(value[1] >= .5):
            cb = self.commands[value[0]]
            cb()
        # Resume speech recognition
        self.asr.pause(False)
        #memory.subscribeToEvent(EVENT_NAME,
        #    MODULE_NAME,
        #    "onWordRecognized")
myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       RobotInfo.getRobotIP(),         # parent broker IP
       RobotInfo.getPort())       # parent broker port

#opponent has verablly announced the end of their turn, get top card on discard pile and trigger FSM events
def endTurnOpp():
    global game_state
    if game_state == "midgame":
        CTemp = ComputerVision.getTopCard(ComputerVision.getVisibleCards())
        val = "" + CTemp[0]
        suit =  "" + CTemp[1]
        absLayer.oppEndTurn.Trigger(val, suit)

#listens for opponent to announce they have won the game at the end of their turn
def playerWins():
    global game_state
    if game_state == "midgame":
        CommandDetector.tts.say("Congratulations")
        game_state = "pregame"

#listen for a player to announce they are shuffling the deck
def deckShuffle():
    global game_state
    if game_state == "midgame":
        CommandDetector.tts.say("Okay")

#Nao listens and records the stated number of players in the game
#this number will not include the Nao
def hearNumPlayers():
##implement ability to hear a number from 1-6
    global game_state
    if game_state == "gamecount":
        n = 1
        temp = ComputerVision.getTopCard(ComputerVision.getVisibleCards())
        ns = " " + str(n)
        absLayer.startgame.trigger(ns, temp[0], temp[1])
        game_state = "midgame"

#Nao listens for the command to start a new game of Crazy 8's
def hearStartGame():
    global game_state
    if game_state == "pregame":
        CommandDetector.tts.say("Alright, starting game! How many people will be playing with me?")
        game_state = "gamecount"

#selects a phrase to say if an opponent is going
def newOpp():
    NextPlayerTurnPhrases = [
        "Okay, your turn",
        "Next player please!",
        "Your turn now!"
    ]
    selected_phrase = random.choice(NaoTurnPhrases)
    tts.say(selected_phrase)

#selects a phrase for the Nao to say if it is now his turn
def NaoGoes():
    NaoTurnPhrases = [
        "Okay, my turn now",
        "I get to go now",
        "Cool, my turn"
    ]
    selected_phrase = random.choice(NextPlayerTurnPhrases)
    tts.say(selected_phrase)

def startCalib(_ = None):
    absLayer.startCalib.trigger()

def continueCalib(_ = None):
    absLayer.nextCalibStep.trigger()

init()

atexit.register(deinit)
#if NaoNext is triggered in FSM, abs layer will make sure NaoGoes() is called
absLayer.NaoNext.subscribe(NaoGoes)
#if oppNext is triggered in FSM, abs layer will make sure newOpp() is called
absLayer.oppNext.subscribe(newOpp)