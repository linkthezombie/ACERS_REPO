from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker
import RobotInfo
import atexit

EVENT_NAME = "WordRecognized"
MODULE_NAME = "CommandDetector"

# Global variable to store the CommandDetector module instance
CommandDetector = None
memory = None

def init():
    global CommandDetector
    
    commands = {
        "Say hi": sayHi,
        "Be nice": compliment,
        "Play a card": sayCard
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

init()

atexit.register(deinit)