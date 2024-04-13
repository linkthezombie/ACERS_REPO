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
Revised 2/19/2024
     - added event calls to suffle
     - removed random TTS calls, replaced with abstraction layer calls (Shelby Jones)
Revised 2/21/2024
     - Fixed bugs to allow games to be played with command detection
Revised 2/26/2024
     - added speech lines and functions for opponent playing crazy 8 (Elise Lovell)
Revised 2/28/2024
     - added a function for opponents to announce they are drawing a card (Nathan Smith)
     - altered playerWins to playerWinsClaim, which triggers logic to check if that is true
Revised 2/29/2024
     - added additional voice commands for opp Crazy 8 (Elise Lovell)
Revised 3/5/2024
     - changed funtion parameters when player ends a turn to allow for new handeling of 8's
Revised 3/10/2024
     - Fixed parameter counts of getTopCard calls and abs layer subscriptions
Revised 3/16/2024
     - added setDifficulty to allow for different levels of play (Elise Lovell)
Revised 3/18/2024
     - added faceForward abs layer calls to hearStartGame and opppEndTurn (Elise Lovell)
Revised 4/2/2024
     - added random selecting of personality at start of game
Revised 4/13/2024
     - added functionality for blackjack included methods and commands (Elise Lovell)
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

#global variable to track game difficulty
game_level = 1

#global variable for personality
persona = 1

def init():
    global CommandDetector

    # The only thing we need this module for is to disable a "listening animation"
    moves = ALProxy("ALAutonomousMoves", RobotInfo.getRobotIP(), RobotInfo.getPort())
    moves.setExpressiveListeningEnabled(False)

    commands = { # List of verbal commands Nao listens out for and the functions triggered after identifying a command

        #game options
        "BlackJack": playBlackjack,
        "Crazy eight's": playCrazyEights,
        
        #Commands to end a player's turn
        "I end my turn": endTurnOpp,
        "I'm done": endTurnOpp,
        "Your turn": endTurnOpp,
        "end turn": endTurnOpp,
        "my turn is over": endTurnOpp,
        #"end": endTurnOpp,
        #"over": endTurnOpp,
        #"done": endTurnOpp,

        #Commands to announce a player has won
        "I win": playerWinsClaim,
        "I won": playerWinsClaim,
        "I have won": playerWinsClaim,
        "We Win": playerWinsClaim,
        "I am victorious!": playerWinsClaim,

        #Commands to announce a player is drawing a card
        "I will draw": playerDraws,
        "I will draw a card": playerDraws,
        "I am drawing": playerDraws,
        "I am drawing a card": playerDraws,
        "I will take a card": playerDraws,

        #Commands to announce the deck is being shuffled
        "I will now shuffle the deck": deckShuffle,
        "I am going to shuffle the deck": deckShuffle,
        "I'm shuffling": deckShuffle,
        "Time to shuffle": deckShuffle,
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
        "Play Game": hearStartGame,

        #Commands for human player changing the suit to spades
        "The suit is now spades": newSuitSpade,
        "I'm making it spades": newSuitSpade,
        "The new suit is spades": newSuitSpade,
        "I pick spades": newSuitSpade,
        "It is spades now": newSuitSpade,

        #Commands for human player changing the suit to clubs
        "The suit is now clubs": newSuitClub,
        "I'm making it clubs": newSuitClub,
        "The new suit is clubs": newSuitClub,
        "I pick clubs": newSuitClub,
        "It is clubs now": newSuitClub,

        #Commands for human player changing the suit to diamonds
        "The suit is now diamonds": newSuitDiamond,
        "I'm making it diamonds": newSuitDiamond,
        "The new suit is diamonds": newSuitDiamond,
        "I pick diamonds": newSuitDiamond,
        "It is dimaonds now": newSuitDiamond,

        #Commands for human player changing the suit to hearts
        "The suit is now hearts": newSuitHeart,
        "I'm making it hearts": newSuitHeart,
        "The new suit is hearts": newSuitHeart,
        "I pick hearts": newSuitHeart,
        "It is hearts now": newSuitHeart,

        #commands for game diffculty levels
        "Easy": setDifficulty,
        "Medium": setDifficulty,
        "Hard": setDifficulty,
        "Easy Mode": setDifficulty,
        "Medium Mode": setDifficulty,
        "Hard Mode": setDifficulty,

        #Blackjack commands
        #Nao's turn
        "Your turn Nao": naoTurn,
        "Nao's turn": naoTurn,
        "Nao can play": naoTurn,

        #end blackjack game
        "Dealer's turn": dealerTurn,
        "Everyone is done": dealerTurn,
        "Game end": dealerTurn,

        #point numbers
        "seventeen": dealerPoints,
        "eighteen": dealerPoints,
        "nineteen": dealerPoints,
        "twenty": dealerPoints,
        "tewnty-one": dealerPoints,
        "twenty-two": dealerPoints,
        "twenty-three": dealerPoints,
        "twenty-four": dealerPoints,
        "twenty-five": dealerPoints,
        "twenty-six": dealerPoints,
        "twenty-seven": dealerPoints,
        "twenty-eight": dealerPoints
        
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
        if value[1] >= .4:
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
    global topCard
    global game_state
    if game_state == "midgame":
        absLayer.faceForward.trigger()
        CTemp = ComputerVision.getTopCard(*ComputerVision.getVisibleCards())
        val = str(CTemp[0])
        suit =  str(CTemp[1])
        temp = ""
        absLayer.oppEndTurn.trigger(val, suit, temp)

# When a player verbally confirms their victory, check if this is true
def playerWinsClaim(_):
    global game_state
    if game_state == "midgame":
        absLayer.oppWonClaim.trigger()

# When a player verbally confirms they are drawing a card, update their card count value
def playerDraws(_):
    global game_state
    if game_state == "midgame":
        absLayer.SayWords.trigger("Okay, draw a card!")
        absLayer.oppDraw.trigger()

# When NaoWon is triggered from the FSM, sets game state to pregame
def naoWins():
    global game_state
    game_state = "pregame"

# When PlayerWon is triggered from the FSM, sets game state to pregame
def oppWins():
    global game_state
    game_state = "pregame"

# When a player verbally calls for a deck shuffle, Nao registers this
def deckShuffle(_):
    global game_state
    if game_state == "midgame":
        absLayer.isShuffled.trigger()
        absLayer.SayWords.trigger("Thank you for shuffling, lets continue.")

#uses player input to determine difficulty at start of game
def setDifficulty(level):
    global game_state
    global game_level
    if game_state == "setupgame":
        if level == "Easy":
            game_level = "1"
        elif level == "Medium":
            game_level = "2"
        else:
            game_level = "3"
        absLayer.SayWords.trigger("Okay! How many players will there be playing with me?")

# When a player verbally states the number of players to participate in the game (exluding Nao), Nao saves this information for later use
def hearNumPlayers(num):
    global game_state
    global game_level
    if game_state == "setupgame":
        n = num[:1] # Pulls the number of players from the command to be passed through the abstraction layer
        temp = ComputerVision.getTopCard(*ComputerVision.getVisibleCards())
        game_state = "midgame"
        absLayer.startGame.trigger([n, str(temp[0]), str(temp[1]), game_level])

#function to set off chain of events if opponent announces they have played an 8 and are changing the suit to hearts
def newSuitHeart(_):
    global topCard
    global game_state
    if game_state == "midgame":
        absLayer.faceForward.trigger()
        CTemp = ComputerVision.getTopCard(*ComputerVision.getVisibleCards())
        suit =  str(CTemp[1])
        absLayer.oppEndTurn.trigger("8", suit, "heart")

#function to set off chain of events if opponent announces they have played an 8 and are changing the suit to clubs
def newSuitClub(_):
    global topCard
    global game_state
    if game_state == "midgame":
        absLayer.faceForward.trigger()
        CTemp = ComputerVision.getTopCard(*ComputerVision.getVisibleCards())
        suit =  str(CTemp[1])
        absLayer.oppEndTurn.trigger("8", suit, "club")

#triggers to let nao know they are going
def naoTurn(_):
    global game_state
    if game_state == "midgame":
        absLayer.faceForward.trigger()
        absLayer.SayWords.trigger("My turn")
        absLayer.turnBlackJack.trigger()

#finish game of blackjack
def dealerTurn(_):
    global game_state
    if game_state == "midgame":
        absLayer.SayWords.trigger("Lets see who won!")
        absLayer.SayWords.trigger("How many points does the dealer have?")

#gets the dealers point total
def dealerPoints(points)
    global game_state
    if game_state == "midgame":
        n = points[:1] # Pulls the number of players from the command to be passed through the abstraction layer
        absLayer.endBlackJack.trigger(n)
        game_state = "pregame"
        
#function to set off chain of events if opponent announces they have played an 8 and are changing the suit to diamonds
def newSuitDiamond(_):
    global topCard
    global game_state
    if game_state == "midgame":
        absLayer.faceForward.trigger()
        CTemp = ComputerVision.getTopCard(*ComputerVision.getVisibleCards())
        suit =  str(CTemp[1])
        absLayer.oppEndTurn.trigger("8", suit, "diamond")

#function to set off chain of events if opponent announces they have played an 8 and are changing the suit to spades
def newSuitSpade(_):
    global topCard
    global game_state
    if game_state == "midgame":
        absLayer.faceForward.trigger()
        CTemp = ComputerVision.getTopCard(*ComputerVision.getVisibleCards())
        suit =  str(CTemp[1])
        absLayer.oppEndTurn.trigger("8", suit, "spade")

#detect command to start a game with the Nao
def hearStartGame(_):
    absLayer.SayWords.trigger("Let's play a game. Do you want to play blackjack or crazy eights?")

#triggers a game of blackjack with voice commands
def playBlackjack(_):
    global game_state
    global persona
    #select random personality
    persona = random.choice([1, 2, 3])
    if game_state == "pregame":
        absLayer.faceForward.trigger()
        absLayer.SayWords("Lets play! I'll get my cards.")
        absLayer.drawBlackJackStart.trigger()
        game_state = "midgame"

# When a player verbally requests to start a game, Nao enters the setup phase for crazy eights
def playCrazyEights(_):
    global game_state
    global persona
    #select random personality
    persona = random.choice([1, 2, 3])
    if game_state == "pregame":
        absLayer.faceForward.trigger()
        absLayer.SayWords.trigger("Alright, starting game! Would you like to play an easy, medium, or hard game?")
        game_state = "setupgame"

def startCalib(_ = None):
    absLayer.startCalib.trigger()

def continueCalib(_ = None):
    absLayer.nextCalibStep.trigger()

init()

atexit.register(deinit)

# If NaoWon is triggered in FSM, abs layer will make sure naoWins is called
absLayer.NaoWon.subscribe(naoWins)
# If NaoWon is triggered in FSM, abs layer will make sure naoWins is called
absLayer.OppWon.subscribe(oppWins)

