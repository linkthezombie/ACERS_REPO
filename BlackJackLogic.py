"""
BlackJackLogic.py

Thinking required for Nao to play BlackJack

Created 4/2/2024
  Edited 4/3/2024 - Elise Lovell
     - added basic funcitonality on turn
  Edited 4/10/2024 - Elise Lovell
    - expanded on framework and broke gameplay into functions
  Edited 4/13/2024 - Elise Lovell
     - cleaned function logic, added calls and triggers and tested
"""
#!/usr/bin/env python2.7

import AbstractionLayer
import hand
from Card import Card

absLayer = AbstractionLayer.AbstractionLayer()
dealerCard = Card("6", "spade")

#start game after everyone is given two cards
#first two are Nao's cards
#last in list is dealer's card
def startGame(dealtCards):
  global dealerCard
  hand.NaoHand = []
  #add all card in starting hand to virtual hand
  ctemp = dealtCards[0]
  hand.addCard(ctemp.vs ,ctemp.ss)
  ctemp = dealtCards[1]
  hand.addCard(ctemp.vs ,ctemp.ss)
  dealerCard = dealtCards[2]
  print("Starting game")

#decide to get new card or not
def hitOrPass():
  if totalHand() >= 17:
    print("I pass")
    absLayer.passTurn.trigger()
  else:
    print("Hit")
    absLayer.hit.trigger()

#add a newly draw card to Nao's hand
def getNewCard(card):
  hand.addCard(card.vs ,card.ss)
  #check if Nao has won or gone over
  if totalHand() == 21:
    print("21!")
    absLayer.done.trigger()
  elif totalHand() > 21:
      print("Bust")
      absLayer.done.trigger()
  else:
    print("Still in")
    hitOrPass()

#determines if Nao won or not
def gameEnd(dealerTot):
  if totalHand() > 21:
    print("I lost")
    absLayer.lostBlackJack.trigger("Bust")
  elif totalHand() == 21:
    if len(hand.NaoHand) == 2:
      if hand.NaoHand[0].value == 1:
        if hand.NaoHand[1].value > 9:
          print("BlackJack")
          absLayer.wonBlackJack.trigger("BlackJack")
        else:
          print("21, I win!")
          absLayer.wonBlackJack.trigger("I won")
      elif hand.NaoHand[0].value > 9:
        if hand.NaoHand[1].value == 1:
          print("BlackJack")
          absLayer.wonBlackJack.trigger("BlackJack")
        else:
          print("21, I win!")
          absLayer.wonBlackJack.trigger("I won")
      else:
          print("21, I win!")
          absLayer.wonBlackJack.trigger("I won")
    else:
        print("21, I win!")
        absLayer.wonBlackJack.trigger("I won")
  elif totalHand() < dealerTot:
    print("The house wins")
    absLayer.lostBlackJack.trigger("The house wins")
  elif totalHand() > dealerTot :
    print("I won")
    absLayer.wonBlackJack.trigger("I won")
  else:
    print("tied")
    absLayer.lostBlackJack.trigger("Tied")

#calcualte sum of all cards in hands
def totalHand():
  sum = 0
  for card in hand.NaoHand:
    #if card is jack, queen, king, or 10, it's value is 10
    if card.value >= 10:
      sum += 10
    #if its an ace, see if making it 11 or 1 will work
    elif card.value == 1:
      if sum + 11 <= 21:
        sum += 11
        print("ace as 11")
      else:
        sum += 1
        print("ace as 1")
    else:
      sum += card.value
  return sum

absLayer.endBlackJack.subscribe(gameEnd)
absLayer.turnBlackJack.subscribe(hitOrPass)
absLayer.hitReturn.subscribe(getNewCard)
absLayer.startBlackJack.subscribe(startGame)
