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

"""

from DataTypes import *
import FSM
import random
import hand


TopCard = Card #stores last known top card
CardsInDrawPile = 52 #tracks cards left in draw pile
NumOfPlayers = 2 #stores total number of players
Players = [] #stores players in array
CardsInDiscardPile = 1


##
#decison making for robot on it's own turn
def turn(): ####What do a and b represent here? -Shelby
    #loop through each card in hand
    for card in hand:
        #if the card is legal to play on to the stack return true
        if (playable(card) == True):
            #if the card is a better option to play or is the first card that is playable, set as current card
            if(choice(currCard, card) or currCard is None):
                currCard = card
    #if there is no playable card in the NAO's hanFaceUpCardd
    if(currCard is None):
        #check if it there are still cards in the deck
        if(cardsInDeck() == True):
            #implement function to draw cards from deck
            drawCard()
        #if there are no avaliable cards, end turn
        else: 
            passTurn()
    #draw card from card to play
    else:
        play(currCard)


def choice(a, b):
    #main logic, must decide whether or not the new card is a better option to playable
    #true if new card is a better choice
    #want to get rid of higher numbers
    if a.Value > b.Value:
        return a
    elif b.Value == a.Value:
        return random.choice([a,b])
    else:
        return b
    
  
def canPlayCard():
    #compares top card of stack, using number and suite, checks the suite and number of the card passed in to see if it is playable
    #eight is always playable
    var = False
    for card in hand.NaoHand:
        if(card.suit == TopCard.suit or card.value == TopCard.value):
            var = True
    return var        
    

def NextPlayer():
    print("Next Player")
    if(Players[len(Players)] == 1):
        Players[len(Players)] = 0
        Players[0] = 1
    else:
        i = 0
        for x in Players:
            if(x == 1):
                Players[i] = 0
                Players[i+1] = 1
            i = i + 1

        #transition to next players turn

def Compare(c): #if the top card on the draw pile is the same as the 
                #   stored value for top card, no change
    if(c.value == TopCard.value and c.suit == TopCard.suit):
        return True
    else:
        return False

def getNumOfCards():
    return len(hand.NaoHand)
        #returns the current number of cards in hand

