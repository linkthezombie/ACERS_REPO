"""
BlackJackLogic.py

Thinking required for Nao to play BlackJack

Created 4/2/2024
  Edited 4/3/2024 - Elise Lovell
     - added basic funcitonality on turn
  Edited 4/10/2024 - Elise Lovell
    - expanded on framework and broke gameplay into functions
  Edited 4/12/2024 - Elise Lovell
     - cleaned function logic, added calls and triggers and tested
  Edited 4/13/2023 - Elise Lovell
    - connected other layers and events
  Edited 4/15/2024 - Nathan Smith
    - added splitHand() for decision making process on when Nao splits starting hand
"""
#!/usr/bin/env python2.7

import AbstractionLayer
import hand
from BlackJackStrategy import getBestMove, Move
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
  #splitHand() # When fully implemented, allows Nao to decide if it wants to split a hand or not, and if so Nao plays two hands in the same round
  print("Starting game")
  absLayer.SayWords.trigger("I'm ready")

# logic to decide whether or not NAO splits a hand
def splitHand():
  card_value = hand.getValues() #access getValues in hand to create an array of the two current card's values
  if card_value[0] == card_value[1]: #if the two cards have the same values, Nao will decide if splitting is a good idea or not
    if card_value[0] == 1 or card_value[0] == 8: #if Nao has two Aces or Eights, ideal splitting cards, Nao will split regardless
      #TODO: Implement splitting action
      pass
    elif card_value[0] == 2 or card_value[0] == 3 or card_value[0] == 7: #if Nao has bad pairs and Dealer has low card displayed, split to improve bad hands
      if dealerCard.value >= 2 and dealerCard.value <= 7:
        #TODO: Implement splitting action
        pass
    if card_value[0] == 6: #if Nao has two sixes and the Dealer has a 6, split hand so Nao can stand on safe hands while Dealer must draw at least one more card and potentially bust
      if dealerCard.value >= 2 and dealerCard.value <= 6:
        #TODO: Implement splitting action
        pass

#decide to get new card or not
def hitOrPass():
  move = getBestMove(hand.NaoHand, dealerCard)

  if move == Move.STAND: #if best available move is to keep current hand, Nao tells the dealer it will pass
    print("I pass")
    absLayer.SayWords.trigger("I'm done, I'll pass")
  elif move == Move.HIT: #if best available move is to obtain another card, Nao asks the dealer for another card
    print("Hit")
    absLayer.SayWords.trigger("Hit")
    absLayer.hit.trigger()
  else:
    print("getBestMove returned a bad value")

#add a newly draw card to Nao's hand
def getNewCard(card):
  hand.addCard(card.vs ,card.ss)
  #check if Nao has won or gone over
  if totalHand() == 21:
    print("21!")
    absLayer.SayWords.trigger("21, I'm done, I'll pass")
  elif totalHand() > 21:
      print("Bust")
      absLayer.SayWords.trigger("Bust, darn it")
  else:
    absLayer.SayWords.trigger("I'm not out yet")
    print("Still in")
    hitOrPass()

#determines if Nao won or not
def gameEnd(dealerTot):
  if totalHand() > 21:
    print("I lost")
    absLayer.SayWords.trigger("Bust, I lost")
  elif totalHand() == 21: #TODO: This may be simplified, and doesn't account for ties when both dealer and player have blackjack
    if len(hand.NaoHand) == 2:
      if hand.NaoHand[0].value == 1:
        if hand.NaoHand[1].value > 9:
          print("BlackJack")
          absLayer.SayWords.trigger("BlackJack, I win!")
        else:
          print("21, I win!")
          absLayer.SayWords.trigger("I win!")
      elif hand.NaoHand[0].value > 9:
        if hand.NaoHand[1].value == 1:
          print("BlackJack")
          absLayer.SayWords.trigger("BlackJack, I win!")
        else:
          print("21, I win!")
          absLayer.SayWords.trigger("I win!")
      else:
          print("21, I win!")
          absLayer.SayWords.trigger("I win!")
    else:
        print("21, I win!")
        absLayer.SayWords.trigger("I win!")
  elif totalHand() < dealerTot:
    print("The house wins")
    absLayer.SayWords.trigger("The house wins")
  elif totalHand() > dealerTot :
    print("I won")
    absLayer.SayWords.trigger("I win!")
  else:
    print("tied")
    absLayer.SayWords.trigger("Tie, the house wins")
  absLayer.SayWords.trigger("Want to play again?")

#calcualte sum of all cards in hands
def totalHand():
  sum = 0
  numAces = 0

  for card in hand.NaoHand:
    if card.value == 1:
      numAces += 1
    else:
      sum += min(card.value, 10)

  for _ in range(numAces):
    if sum + 11 <= 21:
      sum += 11
      print("ace as 11")
    else:
      sum += 1
      print("ace as 1")

  return sum

absLayer.endBlackJack.subscribe(gameEnd)
absLayer.turnBlackJack.subscribe(hitOrPass)
absLayer.hitReturn.subscribe(getNewCard)
absLayer.startBlackJack.subscribe(startGame)
