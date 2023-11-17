"""
FSM.py

Defines what NAO's transitions are as the game is played


Created 10/4/2023
Revised 10/5/2023
    -added bones - Shelby
Revised 10/19/23 - Shelby
    -added winGame functionality, imported gameStrategy functions
    -added win state
    -added transition functionanlity
Revised 10-20-23 - Shelby & Elise
    -added start state functionality
    -added opponent play functionality
Revised 10-22-23 - Shelby
    -syntax and comments
Revised 10-27-23 -Shelby Jones
    -Fixed errors
Revised 10-27-23 - Shelby & Elise
    -fixed flow control and interactivity of methods
Edited 11/3/2023 - Elise Lovell
    -added print statements for debugging
Edited 11/10/2023 - Elise Lovell
    -added interaction for debugging and comments for location to link to other programs
"""


#!/usr/bin/env python2.7

#import AbstractionLayer
import GameStrategy
import hand
import random
from array import array

states = ["start", "opponentPlay", "playing", "drawing", "NaoPlay", "win"]
state = "start"

def win():
    print("\nWin! Woo hoo")
    #end the game
    return 0

def start():
    
    print("Starting Game: \n\n")

    #adds all of Nao's cards in his start hand to his memory
    propogateHandOnStart()
        
    state = random.choice(["drawing", "opponentPlay"]) #decides who plays first
    state = "drawing" #COMMENT OUT WHEN DONE TESTING
    if state == "drawing":
        print("\nNao goes first")
    else:
        print("\nOpponent goes first")
    #Game.Strategy.NumOfPlayers = input("\nHow many players are there (including Nao and yourself): ")
    GameStrategy.NumOfPlayers = 2
    print("\nNumber of Players: " + str(GameStrategy.NumOfPlayers))
    GameStrategy.CardsInDrawPile = 52 - (GameStrategy.NumOfPlayers * 5) - 1 #calculates cards in draw pile
    print("\nCards in draw pile " + str(GameStrategy.CardsInDrawPile))
       
    #Implement receving card from higher abstraction
    #method in either computerVision or abstraction layer to return the card in the discard pile feild
    #current implementation relies on human player inputing what they see
    s = input("\nPlease enter the suit for the top card of the discard pile: ")
    v = input("\nPlease enter the face value for the top card of the discard pile: ")
    while hand.checkValidity(v, s) == False:
        print("Invalid input, please try again\n")
        s = input("\nPlease enter the suit for the top card of the discard pile: ")
        v = input("\nPlease enter the face value for the top card of the discard pile: ")
    C = hand.Card(v, s)
    GameStrategy.TopCard = C
                
    ##Nao needs to store correct number of players
    GameStrategy.CardsInDiscardPile = 1
    print("\nCards in discard pile: " + str(GameStrategy.CardsInDiscardPile))
    #propoagate the array representing who's turn it is
    setPlayerArr()
    
    
def opponentPlay():
    print("Opponent's turn, please compelete turn\n")
        
    #wait for confrimation of player ending turn via voice recognition
    #function to listen called, and wait for true return?
    #from command detection or abstraction layer

    #implementation for human player interaction till computer vision is linked
    #should create card based on return from function in computer vision or abstraction layer
    #should get card in the discard pile field
        

    NewCard = hand.Card(v, s)
        
    if GameStrategy.compare(NewCard) == True:  #if theres NOT a new card in the discard pile
        GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1 #assume player drew card
        print("\nCards in draw pile " + str(GameStrategy.CardsInDrawPile))
        print("Opponent drew card\n")
    else:
        temp = False
        CardsInDrawPile = CardsInDrawPile - 1
        GameStrategy.TopCard = NewCard #store the new card on the pile
        GameStrategy.CardsInDiscardPile = GameStrategy.CardsInDiscardPile+1
        print("\nCards in discard pile: " + str(GameStrategy.CardsInDiscardPile))
        print("Opponent played card\n")
    playerinput = input("\nIf player won, please enter won, else enter next:" )
        
    print("\nThank you for waiting, the next player may go now\n")
        
    GameStrategy.NextPlayer() #transition to next player

    #check if it is Nao's turn
    if(Players[0] == 1):
        state = "NaoPlay"
        return False

    #take voice command at end of player turn, either be turn complete or won, see beinging of statement for where implmenation should be
    #current implementaion to allow for command line interaction
    if playerin.lower() == "won":
        state = "win"

def playing():

    #handles selecting card to play and communciating with other layers
    GameStrategy.turn()
        
    GameStrategy.CardsInDiscardPile = GameStrategy.CardsInDiscardPile+1
    state = "opponentPlay"
    GameStrategy.NextPlayer()
    winGame() #check if wins game

def drawing(card1):

    #function to implment physcially mechansim to draw card
    #trigger event in abstraction layer or robot motion
    #possibly use drawCard() #physicall draw a card
        
    #computer vision
    #should create card based on return from function in computer vision or abastarction layer
    #return card from feild near face

    hand.addCard(card1.value, cards.suit)
        
    GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1
        
    if(GameStrategy.canPlayCard() == True):
        GameStrategy.turn() 
        state = "playing"
    else:
        state = "opponentPlay"
        GameStrategy.NextPlayer()

def NaoPlay():
    if(canPlayCard() == True): 
        state = "playing"
    else:
        state = "drawing"        


def drawCard():
    print("Physically draw card\n")
        ## pysically draw card
            #implement later

def playCard(c):
    #abslayer.drawcard.subscribe(Card?)
    
    print("Physically play card\n")

    #call to camera to locate the desired card as determined by game strategy
    #call to robot motion to pickup and play said card
    #remove card from memory
    hand.removeCard(c.value, c.suit)
    
def winGame(): #checks if NAO has won the game
    if len(hand.NaoHand) == 0:
        state = "win"

def getCurrentState():
    print("Current state: " + str(state) + "\n")
    return state

def setPlayerArr():
    for player in range(GameStrategy.NumOfPlayers):
        GameStrategy.Players.append(0)

    if(state == "drawing"):
        GameStrategy.Players[0] = 1
    else:
        GameStrategy.Players[1] = 1

def propogateHandOnStart():

    #call function in robot motion to draw card
    #call method in abstraction layer or computer vision to indentify card in drawn field

    #do above 5 times 

    #implmentation to allow for command line interaction for testing
    for x in range(5):
        s = input("\nPlease enter the suit for the card Nao drew: ")
        v = input("\nPlease enter the face value for the card Nao drew: ")
        while hand.checkValidity(v, s) == False:
            print("Invalid input, please try again\n")
            s = input("\nPlease enter the suit for the card Nao drew: ")
            v = input("\nPlease enter the face value for the card Nao drew: ")
        hand.addCard(v, s)


GameStrategy.TopCard = hand.Card("K", "spade")

