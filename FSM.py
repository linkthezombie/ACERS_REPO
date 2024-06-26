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
Revised 2/21 - Nathan Smith
     - implementation of functionality after players win a game
     - added lose state
Revised 2/28/2024 - Elise Lovell
    - added function call to turn event
Revised 2/28 - Nathan Smith
     - removed player drawing functionality from opponentPlay, moved to opponentDrew
     - altered opponentPlay to now keep track of the number of cards in players hand
Revised 3/5 - Elise Lovell
     - altered tracking suit when 8
Revised 3/16 - Elise Lovell
     - changes for difficulty levels
"""
#!/usr/bin/env python2.7

import AbstractionLayer
from Card import Card
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
    state = ""
    return 0

#starts the program and set up variables and functions
#takes list with value and suit of the seen card on the discard pile in index 1 and 2 respectively 
#the num of players is index 0
#index 3 it the game difficulty level
def start(list):
    print("Starting Game: \n\n")
    state = "start"
    #adds all of Nao's cards in his start hand to his memory by utlizing the abs layer event to physically draw the
    #first five starting cards
    absLayer.drawStartingHand.trigger()

    GameStrategy.NumOfPlayers = int(list[0]) + 1
    GameStrategy.CardsInDrawPile = 52 - (GameStrategy.NumOfPlayers * 5) - 1 #calculates cards in draw pile

    GameStrategy.gameLevel = int(list[3])

    #populates the player card count array with the number of cards each player starts with
    for _ in range(int(list[0])):
        GameStrategy.PlayerCardCount.append(5)

    #using passed in values, update the stored discard card to the one seen
    C = Card(list[1], list[2])
    GameStrategy.TopCard = C

    #handle/set suitOnEight if crazy 8 is first card in discard pile
    if GameStrategy.TopCard.value == 8:
        GameStrategy.suitOnEight = GameStrategy.TopCard.ss
    else:
        GameStrategy.suitOnEight = ""

    ##Nao needs to store correct number of players
    GameStrategy.CardsInDiscardPile = 1
    print("\nCards in discard pile: " + str(GameStrategy.CardsInDiscardPile))

    #determine who will go first
    state = random.choice(["NaoPlay", "opponentPlay"]) #decides who plays first
    #propoagate the array representing who's turn it is
    setPlayerArr(state)
    absLayer.turnHead.trigger(GameStrategy.Players.index(1), GameStrategy.NumOfPlayers)
    if state == "NaoPlay":
        print("\nNao goes first")
        absLayer.SayWords.trigger("I will go first.")
        NaoPlay()
    else:
        absLayer.SayWords.trigger("The player to my left can play first.")

#updates relevant information after another player has announced they will draw a card
def opponentDrew():
    GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile - 1 # Decrease size of card draw pile
    GameStrategy.PlayerCardCount[GameStrategy.current_player] = GameStrategy.PlayerCardCount[GameStrategy.current_player] + 1 # Increase player hand size by 1
    print("\nCards in draw pile " + str(GameStrategy.CardsInDrawPile))
    print("Opponent drew card\n")

#checks current player's number of cards to see if the player won or not, triggers event based on if they have won or not
def opponentWinClaim():
    if GameStrategy.PlayerCardCount[GameStrategy.current_player] <= 0:
        absLayer.OppWon.trigger()
    else:
        absLayer.oppWonLie.trigger()

#determines what happens after another player has announced they have completed their turn
#takes in two string representing the value and suit of the card seen on the discard pile
def opponentPlay(v, s, eightS):
    print("Opponent's turn, please complete turn\n")
    NewCard = Card(v, s)

    if GameStrategy.compare(NewCard):  #if theres NOT a new card in the discard pile
        #update all varaibles
        print("\nCards in draw pile " + str(GameStrategy.CardsInDrawPile))
        print("Opponent didn't play a card\n")
    else:
        if v == "8":
            GameStrategy.suitOnEight = eightS
        #opp played a card
        #update all variables
        GameStrategy.TopCard = NewCard #store the new card on the pile
        GameStrategy.PlayerCardCount[GameStrategy.current_player] = GameStrategy.PlayerCardCount[GameStrategy.current_player] - 1 # Decrease player hand size by 1
        GameStrategy.CardsInDiscardPile = GameStrategy.CardsInDiscardPile+1
        print("\nCards in discard pile: " + str(GameStrategy.CardsInDiscardPile))
        print("Opponent played card\n")

    GameStrategy.NextPlayer() #transition to next player
    absLayer.turnHead.trigger(GameStrategy.Players.index(1), GameStrategy.NumOfPlayers)
    #check if it is Nao's turn
    if GameStrategy.Players[0] == 1:
        state = "NaoPlay"
        #trigger abs layer event that will let Nao say he has won in commandDetection.py
        GameStrategy.current_player = 0
        absLayer.NaoNext.trigger()
        NaoPlay()
    else:
        #trigger abs layer event that will allow the Nao to tell player something before their turn
        #triggers function in commandDetection.py
        GameStrategy.current_player = GameStrategy.current_player + 1 # Update to next player
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
    #call abstraction layer function to let program know there is a card to be played
    #sets of physical interactions with NAO
    #passes the card object that will be played
    if card.value == 8:
        #pick new suit if the card is an 8
        GameStrategy.suitOnEight = GameStrategy.suitChoice()
    absLayer.playCard.trigger(card, GameStrategy.suitOnEight)
    winGame() #check if nao has won game
    absLayer.turnHead.trigger(GameStrategy.Players.index(1), GameStrategy.NumOfPlayers)
    
#what the Nao does if it must draw a card
#takes in the card object it drew to add to its virtual hand
def drawing(card1):
    state = "drawing"
    #add parameter card to hand
    hand.addCard(card1.vs, card1.ss)
    #update variables
    GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1
    #check if the card drawn can be player
    if GameStrategy.canPlayCard():
        playing()
    else:
        #moves onto next player
        GameStrategy.NextPlayer()
        #triggers abs layer event that will let commandDetection.py know to say something before an opponent goes
        absLayer.turnHead.trigger(GameStrategy.Players.index(1), GameStrategy.NumOfPlayers)
        absLayer.oppNext.trigger()

#starts the Nao's turn and moves flow on turn along
def NaoPlay():
    state = "NaoPlay"
    #checks if the Nao can play a card
    if GameStrategy.canPlayCard():
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
    if n == "NaoPlay":
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
    GameStrategy.CardsInDrawPile = (GameStrategy.CardsInDiscardPile -1) + GameStrategy.CardsInDrawPile
    GameStrategy.CardsInDiscardPile = 1

#calls upon oppWon from AbstractionLayer to reset crucial variables when a player wins
def oppWins():
    state = ""
    hand.NaoHand = []
    # TODO: Add further logic for opponent winning

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

#if opponent wins, oppwins() is triggered to reset state variable to empty
absLayer.OppWon.subscribe(oppWins)

#if opponent draws a card, oppdraw() is triggered to update the size of draw pile and of player hand
absLayer.oppDraw.subscribe(opponentDrew)

#if opponent claims to have won, triggers opponentwinclaim() to check if this is true or not
absLayer.oppWonClaim.subscribe(opponentWinClaim)
