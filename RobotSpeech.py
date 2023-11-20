"""
RobotSpeech.py

Program to enable NAO to communicate ideas and actions during various moments of the game

Created by Nathan Smith

Created 11/20/2023
"""

# Import the necessary modules from the qi library
from naoqi import ALProxy
from hand import NaoHand
import random
import RobotInfo

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

def playCardSpeech(rank, suit):

    # Annouces the card it is playing, and if it is playing an 8 announces the new suit it has chosen
    # TODO implement way of deciding what suit to play based on the cards in NAO's hand, not randomly
    if rank == "8":
        # If the rank is "8", choose a random suit
        random_suit = random.choice(["diamonds", "clubs", "hearts", "spades"])
        phrase = f"I will play the {rank} of {suit}, and I will make the suit {random_suit}."
    else:
        # If the rank is not "8", use the provided suit
        phrase = f"I will play the {rank} of {suit}."

    # TODO alter method of checking how many cards are in the NAO's hand to fit desired interactions
    if NaoHand == []:
        gameWinSpeech()
    else:
        endTurnSpeech()

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