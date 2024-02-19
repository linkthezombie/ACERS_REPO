"""
AbstractionLayer.py

Singleton class with observable events that systems can subscribe to and publish.
Requirement ID 15

Created by Liam McKinney

Created 9/20/2023
Revised 9/29/2023
    -Added comments (Liam McKinney)
Revised 10/19/2023
    -Python 2.7 compatibility (Liam McKinney)
Revised 12/1/2023
    -New events added (Elise Lovell)
Revised 12/2/2023
    -New events added (Elise Lovell)
Revised 1/24/2024
     -edited type of event parameters for startGame to be a list of strings (Elise Lovell)
Revised 1/29/2024
     - added event for robot speech (Elise Lovell)
Revised 2-19-2024 (Shelby Jones)
     -added an event to say anything inputted as a string
"""

from typing import TypeVar, Generic, List, Callable, Tuple
from DataTypes import *

# We use type generic type hints for events to make it easier to
# know what data types to expect during development
T = TypeVar('T')
class Event(Generic[T]):
    # basic initialization
    def __init__(self):
        self.subscribers = [] # type: List[Callable[...,None]]

    # trigger the event, calling all subscriber callbacks
    def trigger(self, *data):
        # type: (Tuple[T]) -> None
        for subCallBack in self.subscribers:
            subCallBack(*data)

    # provide a callback to be called whenever the event triggers
    def subscribe(self, callback):
        # type: (Callable[..., None]) -> None
        self.subscribers.append(callback)

# singleton class to hold all game events
class AbstractionLayer(object):
    #make sure all constructor calls return the same instance
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AbstractionLayer, cls).__new__(cls)
            cls.instance.initEvents()
        return cls.instance

    #initialize events
    def initEvents(self):
        #begin game
        self.startGame = Event[List[str]]()
        self.drawStartingHand = Event[None]()
        self.returnSH = Event[List[Card]]()
        
        #game over commands
        self.oppWon = Event[None]()
        self.NaoWon = Event[None]()
        
        #Robot commands
        self.playCard = Event[Tuple[Card, str]]()
        self.drawCard = Event[None]()

        # Game events - Robot's actions
        self.drewCard = Event[Card]()
        self.playedCard = Event[None]()

        # Player actions
        self.oppEndTurn = Event[Tuple[str, str]]()

        #speech triggers
        self.NaoNext = Event[None]()
        self.oppNext = Event[None]()
        

        self.SayWords = Event[str]() #trigger to say a string

        #calibration process
        self.startCalib = Event[None]()
        self.nextCalibStep = Event[None]()
        
        self.firstTurn = Event[int]()
