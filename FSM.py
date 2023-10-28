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
"""

import AbstractionLayer
import GameStrategy

states = ["start", "opponentPlay", "thinking", "playing", "drawing", "NaoPlay", "win"]
state = ""

def startGame():
    state = "start"
    var = False
    C = Card("9", "Club")
    while var == False:
        var = transition()
    return 0


def transition():
    if state == "win":
        print("\nWin! Woo hoo")
        return True
        #end the game
    elif state == "start": #when the game starts
        print("Starting Game: \n\n")
        state = random.choice(["drawing", "opponentPlay"]) #decides who plays first
        if state == "drawing":
            print("\nNao goes first")
        else:
            print("\nOpponent goes first")
        GameStrategy.NumOfPlayers = 2
        GameStrategy.CardsInDrawPile = 52 - (numOfPlayers * 5) - 1 #calculates cards in draw pile
        GameStrategy.TopCard = C #read in card via computer vision implemented later
        ##Nao needs to store correct number of players
        GameStrategy.CardsInDiscardPile = 1
        ##Nao should announce who's turn it is first
        setPlayerArr()
        #for player in range(GameStrategy.NumOfPlayers):
    elif state == "opponentPlay":
        #wait for confrimation of player ending turn via voice recognition
            #or if top card changes
        if GameStrategy.Compare(NewCard) == True:  #if theres NOT a new card in the draw pile
            GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1 #assume player drew card
        else:
            GameStrategy.TopCard = NewCard #store the new card on the pile
            GameStrategy.CardsInDiscardPile = GameStrategy.CardsInDiscardPile+1
           

        GameStrategy.NextPlayer() #transition to next player

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
        drawCard() #physicall draw a card
        GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1
        if(canPlayCard() == True):
            GameStrategy.turn() 
            state = "playing"
        else:
            state = "opponentPlay"
            GameStrategy.NextPlayer()
        return False

    elif state == "NaoPlay":
        state = "thinking"
        return False

    else:
        print("error Not Valid State")
        return False
        #error


def drawCard():
    print("Pphysically draw card")
        ## pysically draw card
            #implement later
def playCard():
    print("physically play card")
        # pysically play card
            #implement later

def winGame(): #checks if NAO has won the game
    if len(hand.NaoHand) == 0:
        state = "win"

def getCurrentState():
    return state

def setPlayerArr():
        
    for player in GameStrategy.NumOfPlayers:
        GameStrategy.Players.push(0)

    if(state == "drawing"):
        GameStrategy.Players[0] = 1
    else:
        GameStrategy.Players[1] = 1
        