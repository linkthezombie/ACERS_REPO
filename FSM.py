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
        print("\nNumber of Players: " + str(GameStrategy.NumOfPlayers))
        GameStrategy.CardsInDrawPile = 52 - (numOfPlayers * 5) - 1 #calculates cards in draw pile
        print("\nCards in draw pile " + str(GameStrategy.CardsInDrawPile))
        GameStrategy.TopCard = C #read in card via computer vision implemented later
                
        ##Nao needs to store correct number of players
        GameStrategy.CardsInDiscardPile = 1
        print("\nCards in discard pile: " + str(GameStrategy.CardsInDiscardPile))
        ##Nao should announce who's turn it is first
        setPlayerArr()
        return False
        #for player in range(GameStrategy.NumOfPlayers):
    elif state == "opponentPlay":
        print("Opponent's turn\n")
        #wait for confrimation of player ending turn via voice recognition
            #or if top card changes
        if GameStrategy.Compare(NewCard) == True:  #if theres NOT a new card in the draw pile
            GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile-1 #assume player drew card
            print("\nCards in draw pile " + str(GameStrategy.CardsInDrawPile))
            print("Opponent drew card\n")
        else:
            temp = False
            while temp != True:
                s = input("\nOptions: Spade, Heart, Club, Diamond\nPlease pick a suit for the card to be drawn: ")
                if s.lower() == "spade" or s.lower() == "heart" or s.lower() == "club"  or s.lower() == "diamond":
                    temp = True
                else:
                    print("\nPlease enter a valid suit")
            
            temp = False
            while temp != True:
                v = input("\nOptions: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K\nPlease pick a value for the card to be drawn: ")
                if v.lower() == "a" or v.lower() == "2" or v.lower() == "3"  or v.lower() == "4" or v.lower() == "5" or v.lower() == "6" or v.lower() == "7"  or v.lower() == "8" or v.lower() == "9" or v.lower() == "10" or v.lower() == "j"  or v.lower() == "q" or v.lower() == "k":
                    temp = True
                else:
                    print("\nPlease enter a valid face value")
            CardsInDrawPile = CardsInDrawPile - 1
            NewCard = Card(v, s)
            GameStrategy.TopCard = NewCard #store the new card on the pile
            GameStrategy.CardsInDiscardPile = GameStrategy.CardsInDiscardPile+1
            print("\nCards in discard pile: " + str(GameStrategy.CardsInDiscardPile))
            print("Opponent played card\n")
           

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
        temp = False
        while temp != True:
            s = input("\nOptions: Spade, Heart, Club, Diamond\nPlease pick a suit for the card to be drawn: ")
            if s.lower() == "spade" or s.lower() == "heart" or s.lower() == "club"  or s.lower() == "diamond":
                temp = True
            else:
                print("\nPlease enter a valid suit")
                temp = False
        while temp != True:
            v = input("\nOptions: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K\nPlease pick a value for the card to be drawn: ")
            if v.lower() == "a" or v.lower() == "2" or v.lower() == "3"  or v.lower() == "4" or v.lower() == "5" or v.lower() == "6" or v.lower() == "7"  or v.lower() == "8" or v.lower() == "9" or v.lower() == "10" or v.lower() == "j"  or v.lower() == "q" or v.lower() == "k":
                temp = True
            else:
                print("\nPlease enter a valid face value")
        hand.addCard(v, s)
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
    for player in GameStrategy.NumOfPlayers:
        GameStrategy.Players.push(0)

    if(state == "drawing"):
        GameStrategy.Players[0] = 1
    else:
        GameStrategy.Players[1] = 1
        
