"""
DataTypes.py

file to hold any custom data types/classes we define

Created by Liam McKinney

Created 9/20/2023
Revised 10/19/2023
    -Python 2.7 compatibility (Liam McKinney)
"""
from enum import Enum

# Enum representing the suit of a card
class Suit(Enum):
    CLUBS = 1
    HEARTS = 2
    SPADES = 3
    DIAMONDS = 4

# Enum representing the face value of a card
class Value(Enum):
    Val_A = 1
    Val_2 = 2
    Val_3 = 3
    Val_4 = 4
    Val_5 = 5
    Val_6 = 6
    Val_7 = 7
    Val_8 = 8
    Val_9 = 9
    Val_10 = 10
    Val_J = 11
    Val_Q = 12
    Val_K = 13

# class to represent a card from the deck
class Card:
    def __init__(self, suit, val):
        # type: (Suit, Value) -> None
        self.suit = suit
        self.val = val

