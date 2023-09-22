from enum import Enum

class Suit(Enum):
    CLUBS = 1
    HEARTS = 2
    SPADES = 3
    DIAMONDS = 4

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

class Card:
    suit: Suit
    val: Value
    def __init__(self, suit: Suit, val: Value):
        self.suit = suit
        self.val = val

