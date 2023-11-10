"""
FSM.py

Defines what NAO's transitions are as the game is played


Created 10/4/2023
Revised 10/X/2023
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
"""

import AbstractionLayer
import GameStrategy
import hand
import random
from array import array

states = ["start", "opponentPlay", "thinking", "playing", "drawing", "NaoPlay", "win"]
state = ""

def startGame():
    global state
    state = "start"
    var = False
    C = hand.Card("9", "Club")
    while var == False:
        var = transition()
    return 0


def transition():
    global state
    if state == "win":
        print("\nWin! Woo hoo")
        return True
        #end the game
    elif state == "start": #when the game starts
        print("Starting Game: \n\n")
        
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
        return False
    
    elif state == "opponentPlay":
        print("Opponent's turn, please compelete turn\n")
        
        #wait for confrimation of player ending turn via voice recognition
        #function to listen called, and wait for true return?
        #from command detection or abstraction layer

        #implementation for human player interaction till computer vision is linked
        #should create card based on return from function in computer vision or abstraction layer
        #should get card in the discard pile field
        
        s = input("\nPlease enter the suit for the current top card of the discard pile: ")
        v = input("\nPlease enter the face value for the current top card of the discard pile: ")
        while hand.checkValidity(v, s) == False:
            print("Invalid input, please try again\n")
            s = input("\nPlease enter the suit for the top card of the discard pile: ")
            v = input("\nPlease enter the face value for the top card of the discard pile: ")
        NewCard = hand.Card(v, s)
        
        if GameStrategy.compare(NewCard) == True:  #if theres NOT a new card in the draw pile
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

        print("\nThank you for waiting, the next player may go now\n")
        
        GameStrategy.NextPlayer() #transition to next player

        #check if it is Nao's turn
        if(Players[0] == 1):
            state = "NaoPlay"
            return False

    elif state == "thinking":
        if(canPlayCard() == True):
            GameStrategy.turn() 
            state = "playing"
        else:
            state = "drawing"        
        return False

    elif state == "playing":
        playCard() #physically play the card
        GameStrategy.CardsInDiscardPile = GameStrategy.CardsInDiscardPile+1
        state = "opponentPlay"
        GameStrategy.NextPlayer()
        winGame() #check if wins game
        return False

    elif state == "drawing":

        #function to implment physcially mechansim to draw card
        #trigger event in abstraction layer or robot motion
        #possibly use drawCard() #physicall draw a card
        
        #computer vision
        #should create card based on return from function in computer vision or abastarction layer
        #return card from feild near face

        #implementation for human player interaction till computer vision is linked
        s = input("\nPlease enter the suit for the card Nao drew: ")
        v = input("\nPlease enter the face value for the card Nao drew: ")
        while hand.checkValidity(v, s) == False:
            print("Invalid input, please try again\n")
            s = input("\nPlease enter the suit for the card Nao drew: ")
            v = input("\nPlease enter the face value for the card Nao drew: ")
        hand.addCard(v, s)

        GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1
        
        if(GameStrategy.canPlayCard() == True):
            GameStrategy.turn() 
            state = "playing"
        else:
            state = "opponentPlay"
            GameStrategy.NextPlayer()
        return False

    elif state == "NaoPlay":
        print("Nao's turn\n")
        state = "thinking"
        return False

    else:
        print("Error Not Valid State\n")
        return False
        #error


def drawCard():
    print("Physically draw card\n")
        ## pysically draw card
            #implement later
    #hand.addCard(val, suit)

def playCard(c):
    print("Physically play card\n")
    
        # pysically play card
            #implement later
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

GameStrategy.TopCard.suit = "spade"
GameStrategy.TopCard.suit = "K"
startGame()
