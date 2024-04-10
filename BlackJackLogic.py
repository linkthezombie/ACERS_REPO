"""
BlackJackLogic.py

Thinking required for Nao to play BlackJack

Created 4/2/2024
  Edited 4/3/2024 - Elise Lovell
     - added basic funcitonality on turn
  Edited 4/10/2024 - Elise Lovell
    - expanded on framework and broke gameplay into functions
"""
#!/usr/bin/env python2.7

import AbstractionLayer
import hand

absLayer = AbstractionLayer.AbstractionLayer()
dealerSum = 0

#start game after everyone is given two cards
#TO DO: subscribe to event
def startGame(dealtCards, dealerCard):
  #add all card in starting hand to virtual hand
  for card in dealtCard:
    hand.NaoHand.addCard(card.vs ,card.ss)

  #set variable for dealers value of cards
  if dealerCard.vs != "a":
    dealerSum = dealerCard.value
  else:
    #TO DO
    print("")
    #determine what to do with dealer ace
  print("Starting game")

#decide to get new card or not
#TO DO: write code for triggers
#TO DO: write subscirbe that will be triggered with voice command
def hitOrPass():
  if totalHand() >= 17:
    print("I pass")
    absLayer.passTurn.trigger()
  else:
    print("Hit")
    absLayer.hit.trigger()

#add a newly draw card to Nao's hand
#TO DO: write code for subscribe
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
    hitOrPass()

#determines if Nao won or not
#TO DO: fix decsions rules
#TO DO: set up subscribe
def gameEnd(dealerTot):
  if totalHand() > 21:
    print("Busted")
  elif totalHand() < dealerTot and totalHand != 21:
    print("The house wins")
  elif totalHand() > dealerTot :
    print("I won")
  #check for blackjack
  elif True:
    print("Blackjack")
  else:
      print("I got 21")

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
