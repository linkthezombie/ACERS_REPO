"""
RobotSpeech.py

Program to enable NAO to communicate ideas and actions during various moments of the game

Created by Nathan Smith

Created 11/20/2023
Edited 11-20-2023 - Nathan Smith
    -added access to abstraction layer and changes to playCardSpeech to not choose a random suit
Edited 12/2/2023 - Elise Lovell
    -added abs layer comments
Edited 1/24/2024 - Elise Lovell
    - added askNumPlayers
Edited 1/29/2024 - Elise Lovell
     - added whoGoesFirstSpeech()
"""

# Import the necessary modules from the qi library
from naoqi import ALProxy
import hand
import AbstractionLayer
import random
import RobotInfo
import CommandDetection

absLayer = AbstractionLayer.AbstractionLayer()

# Connect to the text-to-speech module
tts = ALProxy("ALTextToSpeech", RobotInfo.getRobotIP(), RobotInfo.getPort())

def drawCardSpeech():
    # Create an array of various ways to announce NAO drawing a card
    alternative_phrases = [
        "I will draw a card.",
        "I will draw.",
        "I will take a card.",
        "I will grab a card.",
        "One more card for me.",
        "I'm taking a card."
    ]
    # Choose a random phrase for the NAO to say
    selected_phrase = random.choice(alternative_phrases)
    # Say the specified drawing card line
    tts.say(selected_phrase)

#has Nao ask aloud how many people, not including himself, are playing the game
def askNumPlayers():
    tts.say("How many people are playing?")
    #command function to hear the number of players should be triggered after he says this

def playCardSpeech(card, heldSuit):

    # Annouces the card it is playing, and if it is playing an 8 announces the new suit it has chosen
    if hand.card.value == 8:
        # If the rank is "8", choose a new suit
        phrase = f"I will play the {hand.card.value} of {hand.card.suit}, and I will make the suit {heldSuit}."
    else:
        # If the rank is not "8", use the provided suit
        phrase = f"I will play the {hand.card.value} of {hand.card.suit}."

def whoGoesFirstSpeech(n):
    if n == 1:
        tts.say("I'm going first.")
    elif n == 0:
        tts.say("The player to my right can go first.")

def endTurnSpeech():
    # Create an array of various ways to announce NAO is ending it's turn
    alternative_phrases = [
        "I pass the turn.",
        "That's the end of my turn.",
        "I finish my turn.",
        "My move is done.",
        "I end my turn.",
        "My turn is complete."
    ]
    # Choose a random phrase for the NAO to say
    selected_phrase = random.choice(alternative_phrases)
    # Say the chosen ending turn line
    tts.say(selected_phrase)

def gameWinSpeech():
    # Create an array of various ways to announce NAO has won
    alternative_phrases = [
        "Victory is mine!",
        "I am the winner!",
        "I have won!"
    ]
    # Choose a random phrase for the NAO to say
    selected_phrase = random.choice(alternative_phrases)
    # Say the specified victory line
    tts.say(selected_phrase)

def gameLostSpeech():
    # Create an array of various ways to announce NAO has lost
    alternative_phrases = [
        "Good game!",
        "Well played!",
        "Nicely done!",
        "Congratulations!"
    ]
    # Choose a random phrase for the NAO to say
    selected_phrase = random.choice(alternative_phrases)
    # Say the specified defeat line
    tts.say(selected_phrase)

#if abs layer is told a card will be played, call playCardSpeech()
absLayer.playCard.subscribe(playCardSpeech)
#if abs layer is told a card should be drawn, call drawCardSpeech()
absLayer.drawCard.subscribe(drawCardSpeech)
#if abs layer is told Nao won, call gameWonSpeech()
absLayer.NaoWon.subscribe(gameWinSpeech)
#if abs layer is told an opponent won, call gameLostSpeech()
absLayer.oppWon.subscribe(gameLostSpeech)
#if firstTurn is triggered, whoGoesFirst() will be called
absLayer.firstTurn.subscribe(whoGoesFirstSpeech)
