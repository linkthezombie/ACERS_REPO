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

#from DataTypes import *
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
def preTurn():
    if gameLevel == 1:
        return turnEasy()
    elif gameLevel == 2:
        return turnMedium()
    else:
        return turnHard()

#strategy to pick turn on easy mode games
def turnEasy():
    global TopCard
    currCard = None
    playableCards = []
    #loop through each card in hand
    for card in hand.NaoHand:
        #call method to check if the card is legal to play on to the stack return true
        if playable(card):
            #make list of all allowed cards
            playableCards.append(card)
    #randomly pick a card to play from playable cards
    currCard = random.choice(playableCards)
    print("Playing card: suit: " + currCard.ss + "value: " + currCard.vs + ".\n")
    TopCard = currCard
    return currCard
    print("Top card: " + TopCard.ss + ", " + TopCard.vs + "\n")

#gamePlay of turn if difficulty = Medium
#playest highest value card in hand
def turnMedium():
    global TopCard
    currCard = None
    #loop through each card in hand
    for card in hand.NaoHand:
        #call method to check if the card is legal to play on to the stack return true
        if playable(card):
            #if first card that is playable
            if currCard is None:
                currCard = card
            #if the card is a better option to play, set as current card
            if choice(currCard, card):
                currCard = card
    #physical motion to play the card, will pass selected card to a higher abstraction level
    print("Playing card: suit: " + currCard.ss + "value: " + currCard.vs + ".\n")
    TopCard = currCard
    return currCard
    print("Top card: " + TopCard.ss + ", " + TopCard.vs + "\n")

#actions on Nao turn if game level set to 3
#play highest card value, but save 8's
def turnHard():
    global TopCard
    currCard = None
    #loop through each card in hand
    for card in hand.NaoHand:
        #call method to check if the card is legal to play on to the stack return true
        if playable(card):
            #if first card that is playable
            if currCard is None:
                currCard = card
            #want to save 8's, so if new card is an 8 and there are other options, don't pick to play
            elif card.value != 8:
                #check if an 8 was already picked, and if it is, reassign to new card
                if currCard.value == 8:
                    currCard = card
                #neither newCard or best option are 8's so find new best option
                elif choice(currCard, card):
                    currCard = card
    #physical motion to play the card, will pass selected card to a higher abstraction level
    print("Playing card: suit: " + currCard.ss + "value: " + currCard.vs + ".\n")
    TopCard = currCard
    return currCard
    print("Top card: " + TopCard.ss + ", " + TopCard.vs + "\n")

#main logic, must decide whether or not the new card is a better option to play
#true if new card(a) is a better choice than older card (b)
#want to get rid of higher numbers and cards where there are more of its suits in Nao's hand
#takes in two card objects, a and b
def choice(a, b):
    #check if a is of higher value
    if a.value > b.value:
        print(b.ss +", " + b.vs + " is lower\n")
        return False
    # same value, different suits
    elif b.value == a.value:
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

    #a is of a lower value
    else:
        print(a.ss +", " + a.vs + " is lower\n")
        return True

#checks if there are any playablel cards at all in Nao's hand and returns true if there are
#a card is playable if it matches the suit or value of the top card in the stack
#eight is always playable
def canPlayCard():
    var = False
    #loop through every card in the stack
    for card in hand.NaoHand:
        if TopCard.value == 8:
            if card.ss == suitOnEight or card.value == TopCard.value:
                var = True
        #is the card has a matching suit or value, set to True since it would be a playable card
        elif card.suit == TopCard.suit or card.value == TopCard.value:
            var = True
            print("There are playable cards\n")
        # if the card is an eight, it is a playable card
        elif card.value == 8:
            var = True
            print("There are playable cards\n")
    return var

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
    if c.value == TopCard.value and c.suit == TopCard.suit:
        print("Top cards do match\n")
        return True
    else:
        print("Top cards don't match\n")
        return False

#takes a card object and return true if the card can be played on the stack
#can be played if it is an 8 or the suit matches or the value matches the card on the top of the discard pile
def playable(c):
    #check if suit or value mactch
    if TopCard.value == 8:
        if c.value == TopCard.value or c.ss == suitOnEight:
            print("Card " + str(c.value) + ", " + str(c.suit) + " is playable\n")
            return True
    elif c.value == TopCard.value or c.suit == TopCard.suit:
        print("Card " + str(c.value) + ", " + str(c.suit) + " is playable\n")
        return True
    #check if card in an eight
    elif c.value == 8:
        print("Card " + str(c.value) + ", " + str(c.suit) + " is playable\n")
        return True
    else:
        print("Card " + str(c.value) + ", " + str(c.suit) + " is not playable\n")
        return False

#makes sure right logic is called for the difficulty level of the game
def preSuitChoice():
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

