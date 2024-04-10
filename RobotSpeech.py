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
Edited 2-28-2024 - Nathan Smith
     - added playerAccuse so that if a player announces their victory before Nao thinks they are out of cards, Nao says so
Edited 3-4-2024 - Shelby Jones
    - added basic casual interactions for Nao to say
"""

# Import the necessary modules from the qi library
from naoqi import ALProxy
import hand
import AbstractionLayer
import random
import RobotInfo
import CommandDetection

absLayer = AbstractionLayer.AbstractionLayer()


###

#persona 1 is kind
#persona 2 is stoic
#persona 3 is snarky / passive-agressive

###

# Connect to the text-to-speech module
tts = ALProxy("ALTextToSpeech", RobotInfo.getRobotIP(), RobotInfo.getPort())

def drawCardSpeech():
    # Create an array of various ways to announce NAO drawing a card
    persona1Draw=[
        "I'm taking a card",
        "I will grab a card"
    ]
    persona2Draw=[
        "I will draw",
        "I will take a card"
    ]
    persona3Draw=[
        "Dang, another card?",
        "One more card for me I guess",
        "one more card to beat you with"
    ]
    # Choose a random phrase for the NAO to say
    if(CommandDetection.persona == 1):
        selected_phrase = random.choice(persona1Draw)

    if(CommandDetection.persona == 2):
        selected_phrase = random.choice(persona2Draw)

    if(CommandDetection.persona == 3):
        selected_phrase = random.choice(persona3Draw)
    # Say the specified drawing card line
    tts.say(selected_phrase)

def playCardSpeech(card, heldSuit):
    #changes variables to be more naturally spoken form
    cardName = card.cardName()

    heldSuit = str(heldSuit) + "s"

    # Annouces the card it is playing, and if it is playing an 8 announces the new suit it has chosen
    if card.value == 8:
        # If the rank is "8", choose a new suit
        phrase = "I will play the %s, and I will make the new suit %s." % (cardName, heldSuit)
    else:
        # If the rank is not "8", use the provided suit
        phrase = "I will play the %s." % (cardName)
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
    persona1Win = [
        "I win! You played a great game",
        "I won! This was fun!"
        "I win! great job"
    ]
    persona2Win=[
        "I have won",
        "I am the winner"
        "I win"
    ]
    persona3Win = [
        "Yes! Victory is mine!",
        "Boohyah, I Win!!"
        "I'm the winner, and you're a loser"
    ]
    # Choose a random phrase for the NAO to say
    if(CommandDetection.persona == 1):
        selected_phrase = random.choice(persona1Win)

    if(CommandDetection.persona == 2):
        selected_phrase = random.choice(persona2Win)

    if(CommandDetection.persona == 3):
        selected_phrase = random.choice(persona3Win)
    # Say the specified victory line
    tts.say(selected_phrase)
    gameRestartSpeech()

def gameLostSpeech():
    # Create an array of various ways to announce NAO has lost
    persona1Lost=[
        "Great job!",
        "Nicely done!"
        "You played a great game"
    ]
    persona2Lost=[
        "Good Game.",
        "Well Played."
        "Good job"
    ]
    persona3Lost=[
        "You must've cheated",
        "Congratulations I guess.",
        "You got lucky, That won't happen again"
    ]
    # Choose a random phrase for the NAO to say
    if(CommandDetection.persona == 1):
        selected_phrase = random.choice(persona1Lost)

    if(CommandDetection.persona == 2):
        selected_phrase = random.choice(persona2Lost)

    if(CommandDetection.persona == 3):
        selected_phrase = random.choice(persona3Lost)
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
    persona1NaoTurn=[
        "Okay, my turn",
        "I get to go next",
        "Good move, My turn!"
    ]
    persona2NaoTurn=[
        "It's my turn",
        "I play now",
        "My turn"
    ]
    persona3NaoTurn=[
        "Finally, It's my turn now",
        "Cool, My turn",
        "I'm One turn closer to beating you"
    ]
    if(CommandDetection.persona == 1):
        selected_phrase = random.choice(persona1NaoTurn)

    if(CommandDetection.persona == 2):
        selected_phrase = random.choice(persona2NaoTurn)

    if(CommandDetection.persona == 3):
        selected_phrase = random.choice(persona3NaoTurn)

    tts.say(selected_phrase)

#selects a phrase to say if an opponent is going
def newOpp():
    persona1NextPlayer=[
        "Next player please!",
        "Okay, your turn",
        "you get to go next"
    ]
    persona2NextPlayer=[
        "Next player",
        "Your turn",
        "Your move"
    ]
    persona3NextPlayer=[
        "I don't have all day, next player go",
        "Next player now",
        "Next player Hurry Up"
    ]
    if(CommandDetection.persona == 1):
        selected_phrase = random.choice(persona1NextPlayer)

    if(CommandDetection.persona == 2):
        selected_phrase = random.choice(persona2NextPlayer)

    if(CommandDetection.persona == 3):
        selected_phrase = random.choice(persona3NextPlayer)

    tts.say(selected_phrase)

#selects a phrase to say if an opponent is caught trying to announce their victory prematurely
def accusePlayer():
    persona1Accuse=[ #kind
        "Sorry, but I think you still have cards left",
        "Are you sure about that?",
        "Not yet, I can see you still have cards."
    ]
    persona2Accuse=[ #stoic
        "That's not true.",
        "You haven't won yet.",
        "That is incorrect"
    ]
    persona3Accuse=[ #snarky
        "Hey, you don't have 0 cards left!",
        "Liar, you still have cards left!"
        "I guess I'm playing with a liar then"
    ]
    if(CommandDetection.persona == 1):
        selected_phrase = random.choice(persona1Accuse)

    if(CommandDetection.persona == 2):
        selected_phrase = random.choice(persona2Accuse)

    if(CommandDetection.persona == 3):
        selected_phrase = random.choice(persona3Accuse)

    tts.say(selected_phrase)

def casualSpeech():
    num = random.randint(1, 10)#chose random number between 1 and 10
    
    persona1Casual = [ #kind
        "You're pretty good at this game",
        "Don't worry, I'm not a cheater!",
        "Isn't this game fun?"
    ]
    persona2Casual = [ #stoic
        "I will not lose",
        "You play this game well"
    ]
    persona3Casual = [ #snarky
        "You Better not be a cheater!",
        "Why don't you just surrender now?",
        "You must enjoy losing"
    ]
    if num%3 == 0: # gives it 3/10 chance to say random phrase
        numCards = len(hand.NaoHand)

        if numCards > 6:
            tts.say("I have a lot of cards")
        elif numCards == 1:
            tts.say("I only have one card left")
        else:
            if(CommandDetection.persona == 1):
                selected_phrase = random.choice(persona1Casual)

            if(CommandDetection.persona == 2):
                selected_phrase = random.choice(persona2Casual)

            if(CommandDetection.persona == 3):
                selected_phrase = random.choice(persona3Casual)

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
absLayer.OppWon.subscribe(gameLostSpeech)
#event playedCard will be triggered and call endTurnSpeach once the Nao has played a card
absLayer.playedCard.subscribe(endTurnSpeech)
#if abs layer is told player said they win early, call accusePlayer to tell them they are wrong
absLayer.oppWonLie.subscribe(accusePlayer)

#if abslayer gets SayWords, it will trigger AnySpeech
absLayer.SayWords.subscribe(anySpeech)
