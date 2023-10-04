"""
FSM.py

Defines what NAO's transitions are as the game is played


Created 10/4/2023
Revised 10/X/2023
    -added bones - Shelby
"""

import AbstractionLayer

states = ["start", "opponentPlay", "thinking", "playing", "drawing"]

class FSM:
    def __init__(self):
        self.state = "start"
    def transition(self, event):
        if self.state == "start":
            #add possible transitions here
        elif self.state == "opponentPlay":
            #wait
        elif self.state == "thinking":
            #transfer to make decision
        elif self.state == "playing":
            #physically play the card
        elif self.state == "drawing":
            #physicall draw a card and add to hand
        else:
            #error
    def drawCard(self):

    def playCard(self):

    def decideCard(self):
    
    def winGame(self):

    def getCurrentState(self):
        return self.state