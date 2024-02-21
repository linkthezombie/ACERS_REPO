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
Edited 12-2-2023 - Elise Lovell
    - connected to commandDecetcion, robotspeech, robotmotion, and other layers
    - functionality to draw five cards at start of game
Edited 1-24-2024 - Elise Lovell
    - functionality for mutiple players added
Revised 1-29-2024 - Elise Lovell
     - debugging
Revised 2/7/2024 - Elise Lovell
     - debugging and managing control flow
Revised 2/17-2/18 - Elise Lovell
     - debugging after running test games
"""
#!/usr/bin/env python2.7

import AbstractionLayer
import GameStrategy
import hand
import random
from array import array

absLayer = AbstractionLayer.AbstractionLayer()
state = ""

#called when the Nao has won
def win():
    print("\nWin! Woo hoo")
    absLayer.NaoWon.trigger()
    #end the game
    #need way to end game and allow for restart
    return 0

#runs to start the program and set up variables and functions
#takes list with the value and suit of the seen card on the discard pile in index 1 and 2 and the num of players in index 0
def start(list):
    print("Starting Game: \n\n")
    state = "start"
    #adds all of Nao's cards in his start hand to his memory by utlizing the abs layer event to physically draw the
    #first five starting cards
    absLayer.drawStartingHand.trigger()
    
    GameStrategy.NumOfPlayers = int(list[0]) + 1
    GameStrategy.CardsInDrawPile = 52 - (GameStrategy.NumOfPlayers * 5) - 1 #calculates cards in draw pile
    
    #using passed in values, update the stored discard card to the one seen
    C = hand.Card(list[1], list[2])
    GameStrategy.TopCard = C
                
    ##Nao needs to store correct number of players
    GameStrategy.CardsInDiscardPile = 1
    print("\nCards in discard pile: " + str(GameStrategy.CardsInDiscardPile))

    #determine who will go first
    state = random.choice(["NaoPlay", "opponentPlay"]) #decides who plays first
    #propoagate the array representing who's turn it is
    setPlayerArr(state)
    if state == "NaoPlay":
        print("\nNao goes first")
        absLayer.SayWords.trigger("I will go first.")
        NaoPlay()
    else:
        absLayer.SayWords.trigger("The player to my right can play first.")
    
#determines what happens after another player has announced they have completed their turn
#takes in two string representing the value and suit of the card seen on the discard pile
def opponentPlay(v, s):
    print("Opponent's turn, please compelete turn\n")
    NewCard = hand.Card(v, s)
        
    if GameStrategy.compare(NewCard) == True:  #if theres NOT a new card in the discard pile
        #update all varaibles
        GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1 #assume player drew card
        print("\nCards in draw pile " + str(GameStrategy.CardsInDrawPile))
        print("Opponent drew card\n")
    else:
        #opp played a card
        #update all variables
        temp = False
        GameStrategy.TopCard = NewCard #store the new card on the pile
        GameStrategy.CardsInDiscardPile = GameStrategy.CardsInDiscardPile+1
        print("\nCards in discard pile: " + str(GameStrategy.CardsInDiscardPile))
        print("Opponent played card\n")
   
    print("\nThank you for waiting, the next player may go now\n")
        
    GameStrategy.NextPlayer() #transition to next player

    #check if it is Nao's turn
    if (GameStrategy.Players[0] == 1):
        state = "NaoPlay"
        #trigger abs layer event that will let Nao say he has won in commandDetection.py
        absLayer.NaoNext.trigger()
        NaoPlay()
    else:
        #trigger abs layer event that will allow the Nao to tell player something before their turn
        #triggers function in commandDetection.py
        absLayer.oppNext.trigger()

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
    newSuit = card.suit
    if card.value == 8:
        #pick new suit if the card is an 8
        newSuit = GameStrategy.suitChoice()
        GameStrategy.TopCard.suit = newSuit
    absLayer.playCard.trigger(card, newSuit)
    


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
        #triggers abs layer event that will let commandDetection.py know to say something before an opponent goes
        absLayer.oppNext.trigger()

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
def setPlayerArr(n):
    GameStrategy.Players = []
    #make spot for each player in the game
    for player in range(GameStrategy.NumOfPlayers):
        GameStrategy.Players.append(0)
    #set Nao to go first
    if(n == "NaoPlay"):
        GameStrategy.Players[0] = 1
    #other player goes first
    else:
        GameStrategy.Players[1] = 1

#adds 5 cards drawn by the NAO to its hand to start the game
#takes in array of 5 cards
def propogateHandOnStart(sh):
    hand.NaoHand = []
    #add the five cards in the array to the virtual hand
    for x in sh:       
        hand.addCard(x.vs, x.ss)

#called upon isShuffled from commandDetection and AbstractionLayer
def nowShuffle():
    GameStrategy.CardsInDrawPile = (CardsInDiscardPile -1) + CardsInDrawPile
    GameStrategy.CardsInDiscardPile = 1

#when drewCard is triggered by other functions, drawing() will be called here
#this will mean a card has been drawn physically and must be added virtually
#it passes a card object
absLayer.drewCard.subscribe(drawing)

#wait for event in abs layer that sends the cards drawn in the starting hand, then calls propogateHandOnStart()
absLayer.returnSH.subscribe(propogateHandOnStart)

#wait for abs layer event to be triggered to start the game and call start()
absLayer.startGame.subscribe(start)

#subscribe to shuffle event to update variables when shuffled
absLayer.isShuffled.subscribe(nowShuffle)

#if opponent announces they have ended their turn, opponentPlay() is subsribed to the abstration layer call to run when that happens
absLayer.oppEndTurn.subscribe(opponentPlay)
