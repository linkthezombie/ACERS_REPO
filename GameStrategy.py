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
"""

#from DataTypes import *
import FSM
import random
import hand
from collections import defaultdict


TopCard = hand.Card("6", "spade") #stores last known top card
CardsInDrawPile = 52 #tracks cards left in draw pile
NumOfPlayers = 2 #stores total number of players
Players = [] #stores players in array
CardsInDiscardPile = 1


#decison making for robot on it's own turn and select a card to play
#function only called if there are playable cards in Nao's hand
def turn(): 
    global TopCard
    currCard = None
    #loop through each card in hand
    for card in hand.NaoHand:
        #call method to check if the card is legal to play on to the stack return true
        if (playable(card) == True):
            #if first card that is playable
            if currCard is None:
                currCard = card
            #if the card is a better option to play, set as current card
            if(choice(currCard, card) == True):
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
    if a.Value > b.Value:
        print(b.ss +", " + b.vs + " is lower\n")
        return False
    # same value, different suits
    elif b.Value == a.Value:
        bSuitNum = 0
        aSuitNum = 0
        #tally up how many of each suit are present in the hand for card a and b
        for c in hand:
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
        return False

#checks if there are any playablel cards at all in Nao's hand and returns true if there are
#a card is playable if it matches the suit or value of the top card in the stack
#eight is always playable
def canPlayCard():
    var = False
    #loop through every card in the stack
    for card in hand.NaoHand:
        #is the card has a matching suit or value, set to True since it would be a playable card
        if(card.suit == TopCard.suit or card.value == TopCard.value):
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
    if(Players[len(Players)-1] == 1):
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
    if(c.value == TopCard.value and c.suit == TopCard.suit):
        print("Top cards do match\n")
        return True
    else:
        print("Top cards don't match\n")
        return False

#takes a card object and return true if the card can be played on the stack
#can be played if it is an 8 or the suit matches or the value matches the card on the top of the discard pile
def playable(c): 
    #check if suit or value mactch
    if(c.value == TopCard.value or c.suit == TopCard.suit):
        print("Card " + str(c.value) + ", " + str(c.suit) + " is playable\n")
        return True
    #check if card in an eight
    elif c.value == 8:
        print("Card " + str(c.value) + ", " + str(c.suit) + " is playable\n")
        return True
    else:
        print("Card " + str(c.value) + ", " + str(c.suit) + " is not playable\n")
        return False
    
def suitChoice():
    suit_counts = defaultdict(int) # Initialize defaultdict to store suit counts
    for card in hand.NaoHand: 
        suit_counts[card.suit] += 1 # Increment the count for the current card's suit in defaultdict
    most_common_suit = max(suit_counts, key=suit_counts.get) # Find the suit with the maximum count using the max function and key argument
    return most_common_suit 


#return the number of cards in the Nao's hand
def getNumOfCards():
    return len(hand.NaoHand)

