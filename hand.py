"""
hand.py

Program to control the adding, removing, storing, and tracking of cards in the robots hand
        Requirement ID 24

Created by Elise Lovell

Created 10/19/2023

Edited 10/21/2023  -Elise Lovell
        Added comments to clarify code
Edited 10/27/2023  - Elise Lovell
    Added main functionality and reordering of instertion into array
Edited 3/10/2024
        Fleshed out hand class to handle integer arguments
"""
#import needed functionality for arrays and classes
from array import array
from Card import Card

#array to store cards
NaoHand = []

#adds a new card to the array
#takes string for value and suit to add to the array
def addCard(v, s):
    #checks if new card is a valid card, if yes, create the card
    c = Card(v, s)

    #checks if the card is already in the hand, if it is, can't add a repeat to the hand
    if c in NaoHand:
        print("\nCard already exists in hand")
        return 0

    print("\nAdding: Suit: "+ s + ", Value: "+ v)
    #check if the card will be the first entry in the array and add
    if len(NaoHand) == 0:
        NaoHand.append(c)

    #insert at front of the array
    elif greater(NaoHand[0], c):
        NaoHand.insert(0, c)

    #insert at back of array
    elif not greater(NaoHand[len(NaoHand)-1], c):
        NaoHand.append(c)

    else:
        #in middle of array, loop through till right location is found
        i = 0
        for x in NaoHand:
            if not greater(c, x):
                NaoHand.insert(i, c)
                return 0
            i += 1

    print("\nAdded to hand")
    return 0

#determine which card is "greater"
#true if c1 is greater, false if c2 is greater
#takes two card objects to compare the value of
#based on suit then face value
def greater(c1, c2):
    if c1.suit == c2.suit:
        return c1.value > c2.value

    return c1.suit > c2.suit

#remove a card from hand
#takes a string value and suit for the card that should be removed
def removeCard(v, s):
    #make a card object
    c = Card(v, s)

    #check if the card in the the hand, if it is not, exit because you can't remove something that isn't there
    if not c in NaoHand:
        print("\nCard isn't in hand")
        return 0

    position = NaoHand.index(c)
    NaoHand.pop(position)
    print("\nRemoved from hand")


#check for valid input matching a real playing card
#inputed value and suit must match a real suit and value for a playing card
#if it doesn't, program returns false
#takes in a string reprsenting the value and another for the suit
def checkValidity(v, s):
    numbers = map(str, range(2, 11))

    validValue = v.lower() in (["a", "j", "q", "k"] + numbers)
    validSuit = s.lower() in ["spade", "club", "diamond", "heart"]

    return validValue and validSuit

#prints array in order
#no post or preconditions
def getHand():
    print("\nHand:")
    #loops through array and prints string value and suit associated with that card
    for x in NaoHand:
        print("\nSuit: " + x.ss + " Value: " + x.vs)

# returns array of card values, ignoring card suits
def getValues():
    values = []
    for x in NaoHand:
        values.append(x.ss)
    return values