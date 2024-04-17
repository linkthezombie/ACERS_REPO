from Card import Card
from enum import Enum

class Move(Enum):
    HIT = 0
    STAND = 1

# Returns the best move to do given a hand and dealer's up card.
def getBestMove(hand, upCard):
    # If you have an ace, the strategy is different
    if handHasAce(hand):
        return getBestMoveWithAce(hand, upCard)
    else:
        return getBestMoveWithoutAce(hand, upCard)

def getBestMoveWithoutAce(hand, upCard):
    handValue = getHandValue(hand)
    upCardValue = getCardValue(upCard)

    if handValue <= 11:
        return Move.HIT

    if handValue >= 17:
        return Move.STAND

    strategy = [
        #    A         2           3           4           5           6           7         8         9        10
        [Move.HIT, Move.HIT,   Move.HIT,   Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT], #12
        [Move.HIT, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT], #13
        [Move.HIT, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT], #14
        [Move.HIT, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT], #15
        [Move.HIT, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.STAND, Move.HIT, Move.HIT, Move.HIT, Move.HIT], #16
    ]
    return strategy[handValue-12][upCardValue-1]

def getBestMoveWithAce(hand, upCard):
    handValue = getHandValue(hand)
    upCardValue = getCardValue(upCard)

    if handValue <= 6:
        return Move.HIT

    if handValue >= 8:
        return Move.STAND

    if upCardValue == 1 | upCardValue == 9 | upCardValue == 10:
        return Move.HIT

    return Move.STAND

def handHasAce(hand):
    clubs = Card("a", "club")
    diamonds = Card("a", "diamond")
    hearts = Card("a", "heart")
    spades = Card("a", "spade")

    return clubs in hand or diamonds in hand or hearts in hand or spades in hand

def getHandValue(hand):
    sum = lambda accumulator, card: accumulator + getCardValue(card)
    return reduce(sum, hand, 0)

def getCardValue(card):
    return min(card.value, 10)
