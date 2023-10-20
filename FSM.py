"""
FSM.py

Defines what NAO's transitions are as the game is played


Created 10/4/2023
Revised 10/X/2023
    -added bones - Shelby
Revised 10/19/23
    -added winGame functionality, imported gameStrategy functions
    -added win state
    -added transition functionanlity
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
        elif self.state == "start":
            self.state = random.choice(["drawing", "opponentPlay"])
            ##Nao should announce who's turn it is first
        elif self.state == "opponentPlay":
            #wait for confrimation of player ending turn
            self.state = "drawing"
        elif self.state == "thinking":
            decideCard(self)
        elif self.state == "playing":
            playCard(self)
        elif self.state == "drawing":
            drawCard(self)
        else:
            #error


    def drawCard(self):
        ##draw card
        self.state = "thinking"
    def playCard(self):
        #play card
        self.state = "opponentPlay"
    def decideCard(self):
        GameStrategy.turn(a,b) #unsure of what a and b represent, but that is how turn is defined
        self.state = "playing"
    def winGame(self):
        if(GameStrategy.cardsInDeck() == false):
            self.state = "win"

    def getCurrentState(self):
        return self.state