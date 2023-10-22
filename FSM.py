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
"""

import AbstractionLayer
import GameStrategy

states = ["start", "opponentPlay", "thinking", "playing", "drawing", "win"]


class FSM:
    def __init__(self):
        self.state = "start"
    def transition(self, event):
        if self.state = "win":
            #end the game
        elif self.state == "start": #when the game starts
            self.state = random.choice(["drawing", "opponentPlay"]) #decides who plays first
            GameStrategy.CardsInDrawPile = 52 - (numOfPlayers * 5) - 1 #calculates cards in draw pile
            GameStrategy.TopCard = Card #read in card via computer vision implemented later
            ##Nao needs to store correct number of players
            GameStrategy.NumOfPlayers = 2
            ##Nao should announce who's turn it is first
            
            #for player in range(GameStrategy.NumOfPlayers):
            if(self.state == "drawing"):
                GameStrategy.Players.push(1)  #nao is represented by 1
                GameStrategy.Players.push(0)  #player is 0
            else:
                GameStrategy.Players.push(0)
                GameStrategy.Players.push(1)
        elif self.state == "opponentPlay":
            #wait for confrimation of player ending turn via voice recognition
                #or if top card changes
            if GameStrategy.Compare(NewCard) == True:  #if theres NOT a new card in the draw pile
                GameStrategy.CardsInDrawPile = GameStrategy.CardsInDrawPile -1 #assume player drew card
            else:
                GameStrategy.TopCard = NewCard #store the new card on the pile
            GameStrategy.NextPlayer() #transition to next player
            self.state = "drawing"
        elif self.state == "thinking":
            decideCard(self)  #decide what card to play
        elif self.state == "playing":
            playCard(self) #physically play the card
        elif self.state == "drawing":
            drawCard(self) #physicall draw a card
        else:
            #error


    def drawCard(self):
        ## pysically draw card
            #implement later
        self.state = "thinking"
    def playCard(self):
        # pysically play card
            #implement later
        self.state = "opponentPlay"
    def decideCard(self): #decide which card to play
        GameStrategy.turn() 
        self.state = "playing"
    def winGame(self): #checks if NAO has won the game
        if(GameStrategy.cardsInDeck() == false):
            self.state = "win"

    def getCurrentState(self):
        return self.state