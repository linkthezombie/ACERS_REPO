"""
GameStrategy.py

Document to define how the game is played given Nao's current state

Created by Shelby Jones

Created 10/2/2023
Revised 10/X/2023
    -added bones
Edited 10/6/2023 - Elise Lovell
    -added potential methods/functionality
Edited 10-19-2023 - Shelby Jones
    -added rough functionality, choice, cardsInDeck
Edited 10-27-23 -Shelby Jones
    -Fixed errors
Edited 10-27-23 -Shelby & Elise
    -Fleshed out Methods
Edited 11/3/2023 - Elise Lovell
    -added methods/functionality and comments and print statements for debugging
Edited 11-17-2023 - Shelby Jones
    -added python 2.7 compatibility
Revised 11-17-2023 - Elise Lovell
     -debugging
Revised 2/17/2024 - Elise Lovell
     - debugging
Revised 2/28/2024 - Nathan Smith
     - added PlayerCardCount and current_player for tracking the number of cards in each player's hand
Revised 3/5 - Elise Lovell
     - altered tracking suit when 8
Revised 3/14 - Elise Lovell
     - added easy mode functions and mode deciding functions
Revised 3/15 - Elise Lovell
     - added medium mode funcitonality
Revised 3/16 - Elise Lovell
     - added hard mode functionality
"""

import FSM
import random
import hand
from collections import defaultdict


TopCard = hand.Card("6", "spade") #stores last known top card
CardsInDrawPile = 52 #tracks cards left in draw pile
NumOfPlayers = 0 #stores total number of players
Players = [] #stores players in array
CardsInDiscardPile = 1 #initializes discard pile, puts top card in pile
PlayerCardCount = [] #tracks number of cards in each player's hand
current_player = 0 #tracks the currently active player
suitOnEight = ""
gameLevel = 2

#determines how to play turn based on set difficulty
def turn():
    if gameLevel == 1:
        return turnEasy()
    elif gameLevel == 2:
        return turnMedium()
    else:
        return turnHard()

#strategy to pick turn on easy mode games
def turnEasy():
    global TopCard

    playableCards = filter(playable, hand.NaoHand)

    #randomly pick a card to play from playable cards
    card = random.choice(playableCards)
    TopCard = card

    print("Playing card: suit: " + card.ss + "value: " + card.vs + ".\n")
    return card

#gamePlay of turn if difficulty = Medium
#playest highest value card in hand
def turnMedium():
    global TopCard

    playableCards = filter(playable, hand.NaoHand)

    #find the best card according to the choice function
    chooseCard = lambda a, b: b if choice(a, b) else a
    card = reduce(chooseCard, playableCards)

    #physical motion to play the card, will pass selected card to a higher abstraction level
    print("Playing card: suit: " + card.ss + "value: " + card.vs + ".\n")
    TopCard = card
    return card

#actions on Nao turn if game level set to 3
#play highest card value, but save 8's
def turnHard():
    global TopCard

    playableCards = filter(playable, hand.NaoHand)

    notAnEight = lambda c: c.value != 8
    preferableCards = filter(notAnEight, playableCards)

    #avoid playing eights if possible
    if len(preferableCards) > 0:
        playableCards = preferableCards

    #find the best card according to the choice function
    chooseCard = lambda a, b: b if choice(a, b) else a
    card = reduce(chooseCard, playableCards)

    #physical motion to play the card, will pass selected card to a higher abstraction level
    print("Playing card: suit: " + card.ss + "value: " + card.vs + ".\n")
    TopCard = card
    return card

#main logic, must decide whether or not the new card is a better option to play
#true if new card(b) is a better choice than older card (a)
#want to get rid of higher numbers and cards where there are more of its suits in Nao's hand
#takes in two card objects, a and b
def choice(a, b):
    #if values aren't equal, choose the higher value
    if a.value != b.value:
        return b.value > a.value

    bSuitNum = 0
    aSuitNum = 0
    #tally up how many of each suit are present in the hand for card a and b
    for c in hand.NaoHand:
        if c.suit == b.suit:
            bSuitNum = bSuitNum + 1
        elif c.suit == a.suit:
            aSuitNum = aSuitNum + 1

    #if there are more of a's suit in Nao's hand, return true, else false
    if aSuitNum > bSuitNum:
        print(b.ss +", " + b.vs + " is lower\n")
        return False
    else:
        print(a.ss +", " + a.vs + " is lower\n")
        return True

#checks if there are any playable cards at all in Nao's hand and returns true if there are
#a card is playable if it matches the suit or value of the top card in the stack
#eight is always playable
def canPlayCard():
    playableCards = filter(playable, hand.NaoHand)
    return len(playableCards) > 0

#sets the array representing the players turn be be the next players turn
def NextPlayer():
    print("Next Player\n")
    #edge case, if last player in the array finshed their turn, loop back around to the front
    print(len(Players))
    if Players[len(Players)-1] == 1:
        Players[len(Players)-1] = 0
        Players[0] = 1
    #find the current player, set them to 0 and make the player after them one
    else:
        #find current player, set them to 0, set next player to 1
        i = Players.index(1)
        Players[i] = 0
        Players[i+1] = 1
    print("Player "+ str(Players.index(1)) + "'s turn.\n")

#if the top card on the draw pile is the same as the stored variable representing the top card, return true
#takes in a card object from the camera that is on the top of the stack
def compare(c):
    return c == TopCard

#returns the game value of the top card.
#if it is an eight, this will return the chosen suit rather than the literal suit.
def topCardSuit():
    if TopCard.value == 8:
        return suitOnEight
    else:
        return TopCard.suit

#takes a card object and return true if the card can be played on the stack
#can be played if it is an 8 or the suit matches or the value matches the card on the top of the discard pile
def playable(c):
    if c.value == 8:
        return True

    suitsMatch = c.ss == topCardSuit()
    valuesMatch = c.value == TopCard.value

    return suitsMatch or valuesMatch

#makes sure right logic is called for the difficulty level of the game
def suitChoice():
    if gameLevel == 1:
        return suitChoiceEasy()
    elif gameLevel == 2:
        return suitChoiceMedium()
    else:
        return suitChoiceHard()

#randomly picks an suit if Nao plays an 8, on easy mode
def suitChoiceEasy():
    arr = ["spade", "heart", "diamond", "club"]
    return random.choice(arr)

#decide suit to play on 8 for medium level difficulty
#picks suit of highest numbered card in hand
def suitChoiceMedium():
    maxValue = lambda a, b: a if a.value > b.value else b
    return reduce(maxValue, hand.NaoHand).ss

#pick suit on 8 for hard difficulty
#pick suit with most cards in hand
def suitChoiceHard():
    counts = {"spade": 0, "heart": 0, "diamond": 0, "club": 0}

    #count each suit in hand
    for card in hand.NaoHand:
        counts[card.ss] += 1

    #return the largest suit
    maxSuit = lambda a, b: a if counts[a] > counts[b] else b
    return reduce(maxSuit, counts)

#return the number of cards in the Nao's hand
def getNumOfCards():
    return len(hand.NaoHand)

