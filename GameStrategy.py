"""
GameStrategy.py

Document to define how the game is played given Nao's current state

Created by Shelby Jones

Created 10/2/2023
Revised 10/X/2023
    -added bones
Edited 10/6/2023 - Elise Lovell
    -added potential methods/functionality
"""

from DataTypes import *


NaoCards = ["""list of cards"""] #an array to hold the current cards in Nao's hand
PlayableCards = [] #an array for the playable cards for the current state
FaceUpCard = Card


def makeMove:
    when(oppPlayed):

    #Nao Assesses current face-up card
    #Nao makes play decision
    #Nao makes game action, either playing or passing
    #Nao Ends turn

##
#decison making for robot on it's own turn
def turn(a, b):
#loop through each card in hand
    for card in hand:
        #if the card is legal to play on to the stack return true
        if (playable(card) == True):
            #if the card is a better option to play or is the first card that is playable, set as current card
            if(choice(currCard, card) or currCard is None):
                currCard = card
    #if there is no playable card in the NAO's hand
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
    
    
def cardsInDeck():
    #must be able to return a boolean stating whether there are cards left in the deck or not
    #will need to either do this visually or possibly have an integer keeping track of the number of cards in play and in the stack
    
def choice(Card a, Card b):
    #main logic, must decide whether or not the new card is a better option to playable
    #true if new card is a better choice
    #want to get rid of higher numbers
        
    
def playable(Card c):
    #compares top card of stack, using number and suite, checks the suite and number of the card passed in to see if it is playable
    #eight is always playable
    if(c.num == 8):
        return True
    
def drawCard():
    #call to phyiscal function to move robot to locate, and draw a card from deck
    #indendify card, and add to list of current cards in hand, then physically put card in hand
    #set game state to opponents turn
    
def passTurn():
    #call to functions so robot can verablly signal it is done with it's turn, set game state to opponets turn
    
def play(Card c):
        #remove card from list of current cards in hand
        #physically remove card from hand and place on stack, announce end of turn
        #set game state to opponents turn



