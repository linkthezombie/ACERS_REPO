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
Edited 2/11/2024 - Elise Lovell
     - moved functions from CommandDetection, removed askNumPlayers, subscribed to playedCard
Revised 2-19-2024 - Shelby Jones
     - added function to say anything passed in as a string, added abstraction layer subscriptions
Revised 2-21-2024 - Nathan Smith
     - added gameRestartSpeech so that after Nao wins or loses, they ask the player if they wish to play again
Edited 2-27-2024 - Elise Lovell
     - added functionality to make saying the card played more natural
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

def playCardSpeech(card, heldSuit):
    #changes variables to be more naturally spoken form
    value = card.vs
    suit = card.ss + "s"
    if (value = "a"):
        value = "ace"
    elif(value = "q"):
        value = "queen"
    elif(value = "j"):
        value = "jack"
    elif(value = "k"):
        value = "king"

    heldsuit = heldsuit + "s"
    
    # Annouces the card it is playing, and if it is playing an 8 announces the new suit it has chosen
    if card.value == 8:
        # If the rank is "8", choose a new suit
        phrase = "I will play the %s of %s, and I will make the new suit %s." % (value, suit, heldSuit)
    else:
        # If the rank is not "8", use the provided suit
        phrase = "I will play the %s of %s." % (value, suit)
    tts.say(phrase)

def endTurnSpeech():
    # Create an array of various ways to announce NAO is ending it's turn
    alternative_phrases = [
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
    gameRestartSpeech()

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
    gameRestartSpeech()

def gameRestartSpeech():
    # Create an array of various ways to ask the player if they want to play again
    alternative_phrases = [
        "Would you like to play again?",
        "Do you want to play another round?",
        "How about another round?",
        "Do you want to play again?"
    ]
    # Choose a random phrase for the NAO to say
    selected_phrase = random.choice(alternative_phrases)
    # Say the specified defeat line
    tts.say(selected_phrase)

#selects a phrase for the Nao to say if it is now his turn
def NaoGoes():
    NaoTurnPhrases = [
        "Okay, my turn now",
        "I get to go now",
        "Cool, my turn"
    ]
    selected_phrase = random.choice(NaoTurnPhrases)
    tts.say(selected_phrase)

#selects a phrase to say if an opponent is going
def newOpp():
    NextPlayerTurnPhrases = [
        "Okay, your turn",
        "Next player please!",
        "Your turn now!"
    ]
    selected_phrase = random.choice(NextPlayerTurnPhrases)
    tts.say(selected_phrase)

def anySpeech(wordsToSay):
    #say things passed through SayWords in AbsLayer
    tts.say(wordsToSay)



#if oppNext is triggered in FSM, abs layer will make sure newOpp() is called
absLayer.oppNext.subscribe(newOpp)
#if NaoNext is triggered in FSM, abs layer will make sure NaoGoes() is called
absLayer.NaoNext.subscribe(NaoGoes)
#if abs layer is told a card will be played, call playCardSpeech()
absLayer.playCard.subscribe(playCardSpeech)
#if abs layer is told a card should be drawn, call drawCardSpeech()
absLayer.drawCard.subscribe(drawCardSpeech)
#if abs layer is told Nao won, call gameWonSpeech()
absLayer.NaoWon.subscribe(gameWinSpeech)
#if abs layer is told an opponent won, call gameLostSpeech()
absLayer.oppWon.subscribe(gameLostSpeech)
#event playedCard will be triggered and call endTurnSpeeach once the Nao has played a card
absLayer.playedCard.subscribe(endTurnSpeech)

#if abslayer gets SayWords, it will trigger AnySpeech
absLayer.SayWords.subscribe(anySpeech)
