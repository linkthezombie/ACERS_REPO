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
Revised 2/6/24
    -added phrases to command library, added bones to allow game setup
Revised 2/11/24
    - added naoWins function to account for game_state variable not being updated in situations where Nao wins the game (Nathan Smith)
Revised 2/11/2024
    - moved functions to RobotSpeech (Elise Lovell)
Revised 2/19/2023
     - added event calls to suffle
     - removed random TTS calls, replaced with abstraction layer calls (Shelby Jones)
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

# Global variable to track the gamestate for command activation purposes
game_state = "pregame"
tts = None

def init():
    global CommandDetector

    # The only thing we need this module for is to disable a "listening animation"
    moves = ALProxy("ALAutonomousMoves", RobotInfo.getRobotIP(), RobotInfo.getPort())
    moves.setExpressiveListeningEnabled(False)

    commands = { # List of verbal commands Nao listens out for and the functions triggered after identifying a command

        #Commands to end a player's turn
        "I end my turn": endTurnOpp,
        "end turn": endTurnOpp,
        "my turn is over": endTurnOpp,
        "end": endTurnOpp, 
        "over": endTurnOpp,
        "done": endTurnOpp,

        #Commands to announce a player has won
        "I win": playerWins,
        "I have won": playerWins, 
        "We Win": playerWins,
        "I am victorious!": playerWins,

        #Commands to announce the deck is being shuffled
        "I will now shuffle the deck": deckShuffle,
        "I am going to shuffle the deck": deckShuffle,
        "Shuffling": deckShuffle,

        #Commands to determine how many people are playing the game with Nao
        "1 player": hearNumPlayers,
        "2 players": hearNumPlayers,
        "3 players": hearNumPlayers, 
        "4 players": hearNumPlayers, 
        "5 players": hearNumPlayers,
        "6 players": hearNumPlayers,

        #Commands to start/continue the board setup/calibration process
        "Begin calibration": startCalib,
        "Next step": continueCalib,

        #Commands to start a new game or play again at the end of a game
        "Play Again": hearStartGame,
        "Start Game": hearStartGame,
        "Play Crazy Eights": hearStartGame,
        "Play Game": hearStartGame,
        "Play Cards": hearStartGame
        
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
        # If confidence is high enough, run the command
        if(value[1] >= .5):
            cb = self.commands[value[0]]
            cb(value[0])
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

# When a player verbally confirms the end of their turn, get top card on discard pile and trigger FSM events
def endTurnOpp(_):
    global game_state
    if game_state == "midgame":
        CTemp = ComputerVision.getTopCard(ComputerVision.getVisibleCards())
        val = "" + CTemp[0]
        suit =  "" + CTemp[1]
        absLayer.oppEndTurn.Trigger(val, suit)

# When a player verbally confirms their victory, update game state
def playerWins(_):
    global game_state
    if game_state == "midgame":
        game_state = "pregame"

# When NaoWon is triggered from the FSM, sets game state to pregame
def naoWins(_):
    global game_state
    game_state = "pregame"

# When a player verbally calls for a deck shuffle, Nao registers this
def deckShuffle(_):
    global game_state
    if game_state == "midgame":
        absLayer.isShuffled.trigger()
        absLayer.SayWords.trigger("Thank you for shuffling, lets continue.")

# When a player verbally states the number of players to participate in the game (exluding Nao), Nao saves this information for later use
def hearNumPlayers(num):
    global game_state
    if game_state == "setupgame":
        n = num[:1] # Pulls the number of players from the command to be passed through the abstraction layer
        temp = ComputerVision.getTopCard(ComputerVision.getVisibleCards())
        absLayer.startgame.trigger(n, temp[0], temp[1])
        game_state = "midgame"

# When a player verbally requests to start a game, Nao enters the setup phase 
def hearStartGame(_):
    global game_state
    if game_state == "pregame":
        absLayer.SayWords.trigger("Alright, starting game! How many people will be playing with me?")
        game_state = "setupgame"

def startCalib(_ = None):
    absLayer.startCalib.trigger()

def continueCalib(_ = None):
    absLayer.nextCalibStep.trigger()

init()

atexit.register(deinit)

# If NaoWon is triggered in FSM, abs layer will make sure naoWins is called
absLayer.NaoWon.subscribe(naoWins)

