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
Edited 11-15-2023 - Shelby and Elise
    -changed FSM format for compatability with abstraction layer
Edited 11-17-2023 - Shelby Jones    
    -added python 2.7 compatibility
Edited 11-17-2023 - Elise Lovell
    -debugging
Edited 11-19-2023 - Elise Lovell
     - added abstraction layer calls
"""
#!/usr/bin/env python2.7

import AbstractionLayer
import GameStrategy
import hand
import random
from array import array

absLayer = AbstractionLayer.AbstractionLayer()
state = ""

def win():
    print("\nWin! Woo hoo")
    #end the game
    return 0

def start():
    print("Starting Game: \n\n")
    state = "start"
    #adds all of Nao's cards in his start hand to his memory
    propogateHandOnStart()
        
    state = random.choice(["NaoPlay", "opponentPlay"]) #decides who plays first
    state = "NaoPlay" #COMMENT OUT WHEN DONE TESTING
    if state == "NaoPlay":
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
    #part of later sprint
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

#determines what happens after another player has announced they have completed their turn
def opponentPlay():
    print("Opponent's turn, please compelete turn\n")
        
    #wait for confrimation of player ending turn via voice recognition
    #function to listen called, and wait for true return?
    #from command detection or abstraction layer

    #implementation for human player interaction till passing discard pile card to lower abstraction is implemented
    #implemented in later sprint
    s = input("\nPlease enter the suit for the current top card of the discard pile: ")
    v = input("\nPlease enter the face value for the current top card of the discard pile: ")
    while hand.checkValidity(v, s) == False:
        print("Invalid input, please try again\n")
        s = input("\nPlease enter the suit for the top card of the discard pile: ")
        v = input("\nPlease enter the face value for the top card of the discard pile: ")
    NewCard = hand.Card(v, s)
        
    if GameStrategy.compare(NewCard) == True:  #if theres NOT a new card in the discard pile
        #update all varaibles
        GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1 #assume player drew card
        print("\nCards in draw pile " + str(GameStrategy.CardsInDrawPile))
        print("Opponent drew card\n")
        #abstraction layer call to oppDrew to signal they drew a card and set of chain of events
        absLayer.oppDrew.trigger()
    else:
        #opp played a card
        #update all variables
        temp = False
        CardsInDrawPile = CardsInDrawPile - 1
        GameStrategy.TopCard = NewCard #store the new card on the pile
        GameStrategy.CardsInDiscardPile = GameStrategy.CardsInDiscardPile+1
        print("\nCards in discard pile: " + str(GameStrategy.CardsInDiscardPile))
        print("Opponent played card\n")
        #abstraction layer call to oppPlayed to signal they played a card and set of chain of events
        #takes in the card that was played as a parameter
        absLayer.oppPlayed.trigger(GameStrategy.TopCard)
    playerinput = input("\nIf player won, please enter won, else enter next:" )
        
    print("\nThank you for waiting, the next player may go now\n")
        
    GameStrategy.NextPlayer() #transition to next player

    #take voice command at end of player turn, either be turn complete or won, see beinging of statement for where implmenation should be
    #current implementaion to allow for command line interaction
    if playerinput.lower() == "won":
        state = "win"
    #check if it is Nao's turn
    elif (GameStrategy.Players[0] == 1):
        state = "NaoPlay"
        NaoPlay()

#actions the Nao must take if it is going to play a card
def playing():
    state = "playing"
    #handles selecting card to play and communciating with other layers
    card = GameStrategy.turn()
    #remove the played card from virtual hand
    hand.removeCard(card.vs, card.ss)
    #update variables
    GameStrategy.CardsInDiscardPile = GameStrategy.CardsInDiscardPile+1
    #change to next player
    GameStrategy.NextPlayer()
    winGame() #check if wins game
    #call abstraction layer function to let program know there is a card to be played
    #sets of physical interactions with NAO
    #passes the card object that will be played
    absLayer.playCard.trigger(card)


#what the Nao does if it must draw a card
#takes in the card object it drew to add to its virtual hand
def drawing(card1):
    state = "drawing"
    #add parameter card to hand
    hand.addCard(card1.vs, card1.ss)
    #update variables
    GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1
    #check if the card drawn can be player
    if(GameStrategy.canPlayCard() == True):
        playing()
    else:
        #moves onto next player
        GameStrategy.NextPlayer()

#starts the Nao's turn and moves flow on turn along
def NaoPlay():
    state = "NaoPlay"
    #checks if the Nao can play a card
    if(GameStrategy.canPlayCard() == True): 
        state = "playing"
        playing()
    #the Nao must draw a card
    else:
        state = "drawing"
        #triggers drawCard function is abstraction layer to make the NAO draw a card
        #this starts the processes of physically drawing a card
        absLayer.drawCard.trigger()        
    
def winGame(): #checks if NAO has won the game
    if len(hand.NaoHand) == 0:
        state = "win"
        win()

#set up the player array at the start of the game for all players and who will be going first
def setPlayerArr():
    #make spot for each player in the game
    for player in range(GameStrategy.NumOfPlayers):
        GameStrategy.Players.append(0)
    #set Nao to go first
    if(state == "NaoPlay"):
        GameStrategy.Players[0] = 1
    #other player goes first
    else:
        GameStrategy.Players[1] = 1

#adds 5 cards drawn by the NAO to its hand to start the game
def propogateHandOnStart():

    #must command NAO to draw, then see and return a card
    #do above 5 times
    #immplemented in later sprint

    #implmentation to allow for command line interaction for testing by adding five cards from user
    for x in range(5):       
        s = input("\nPlease enter the suit for the card Nao drew: ")
        v = input("\nPlease enter the face value for the card Nao drew: ")
        while hand.checkValidity(v, s) == False:
            print("Invalid input, please try again\n")
            s = input("\nPlease enter the suit for the card Nao drew: ")
            v = input("\nPlease enter the face value for the card Nao drew: ")
        hand.addCard(v, s)

#when drewCard is triggered by other functions, drawing() will be called here
#this will mean a card has been drawn physically and must be added virtually
#it passes a card object
absLayer.drewCard.subscribe(drawing)

#if opponent announces they have ended their turn, opponentPlay() is subsribed to the abstration layer call to run when that happens
#absLayer.oppTurn.subscribe(opponentPlay)
