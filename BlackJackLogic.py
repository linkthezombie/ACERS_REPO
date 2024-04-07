"""
BlackJackLogic.py

Thinking required for Nao to play BlackJack

Created 4/2/2024
  Edited 4/3/2024 - Elise Lovell
     - added basic funcitonality on turn
"""
#!/usr/bin/env python2.7

import AbstractionLayer
import hand

absLayer = AbstractionLayer.AbstractionLayer()

def startGame():
  print("Starting game")

#abs layer subscribe
def hitOrPass():
  if totalHand() >= 17:
    print("I pass")
    absLayer.passTurn.trigger()
  else:
    print("Hit")
    absLayer.hit.trigger()

#abs layer subscribe
#add a newly draw card to Nao's hand
def getNewCard(card):
  hand.NaoHand.addCard(card.vs ,card.ss)
  #check if Nao has won or gone over
  if totalHand() == 21:
    print("I win!")
    absLayer.wonBlackJack.trigger()
  elif totalHand() > 21:
      print("I lose")
      absLayer.lostBlackJack.trigger()
  else:
    print("I'm still playing")
    #abs layer call

#calcualte sum of all cards in hands
def totalHand():
  sum = 0
  for card in hand.NaoHand:
    #if card is jack, queen, king, or 10, it's value is 10
    if card.value >= 10:
      sum += 10
    #if its an ace, see if making it 11 or 1 will work
    elif card.vs == "a":
      if sum + 11 <= 21:
        sum += 11
        print("ace as 11")
      else:
        sum += 1
        print("ace as 1")
    else:
      sum += card.value
  return sum

absLayer.turnBlackJack.subscribe(hitOrPass)
absLayer.hitReturn.subscribe(getNewCard)
