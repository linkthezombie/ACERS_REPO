from typing import TypeVar, Generic, List, Callable
from DataTypes import *

T = TypeVar('T')

class Event(Generic[T]):
    subscribers: List[Callable[[T],None]]
    def __init__(self):
        self.subscribers = []

    def trigger(self, data: T) -> None:
        for subCallBack in self.subscribers:
            subCallBack(data)

    def subscribe(self, callback: Callable[[T], None]) -> None:
        self.subscribers.append(callback)

class AbstractionLayer:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AbstractionLayer, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.playCard = Event[int]()
        self.drawCard = Event[None]()

        self.drewCard = Event[Card]()
        self.playedCard = Event[None]()

        self.oppDrew = Event[None]()
        self.oppPlayed = Event[Card]()