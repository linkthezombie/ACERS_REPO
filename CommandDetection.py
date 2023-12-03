
from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker
import RobotInfo
import atexit
import FSM
import ComputerVision

EVENT_NAME = "WordRecognized"
MODULE_NAME = "CommandDetector"

absLayer = AbstractionLayer.AbstractionLayer()

# Global variable to store the CommandDetector module instance
CommandDetector = None
memory = None

def init():
    global CommandDetector
    
    commands = {
        #test commands
        "Say hi": sayHi,
        "Be nice": compliment,
        "Play a card": sayCard,

        #commands to end a player's turn
        "I end my turn": endTurn,
        "end turn": endTurn,
        "my turn is over": endTurn,
        "end": endTurn, 
        "over": endTurn,
        "done": endTurn
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

def sayHi():
    CommandDetector.tts.say("Hello")

def compliment():
    CommandDetector.tts.say("no")

def sayCard():
    CommandDetector.tts.say("I play the Ace of Spades")

#oppoent has verablly announced the end of their turn, get top card on discard pile and trigger FSM events
def endTurnOpp():
    CTemp = ComputerVision.getTopCard(ComputerVision.getVisibleCards())
    val = "" + CTemp[0]
    suit =  "" + CTemp[1]
    absLayer.oppEndTurn.Trigger(val, suit)

#selects a phrase to say if an opponent is going
def newOpp():
    NextPlayerTurnPhrases = [
        "Okay, your turn",
        "Next player please!",
        "Your turn now!"
    ]
    selected_phrase = random.choice(NaoTurnPhrases)
    tts.say(selected_phrase)

#selects a pharse for the Nao to say if it is now his turn
def NaoGoes():
        NaoTurnPhrases = [
        "Okay, my turn now",
        "I PLAY NOW",
        "Cool, my turn"
    ]
    selected_phrase = random.choice(NextPlayerTurnPhrases)
    tts.say(selected_phrase)

init()

atexit.register(deinit)

#if NaoNext is triggered in FSM, abs layer will make sure NaoGoes() is called
absLayer.NaoNext.subscribe(NaoGoes)
#if oppNext is triggered in FSM, abs layer will make sure newOpp() is called
absLayer.oppNext.subscribe(newOpp)
