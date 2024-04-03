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
#import array
from array import array
# ab_classes.py

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
    numbers = list(map(str, range(2, 11)))

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

#Card class for creating a card with a suit and face value
#preconditions - a value and suit for the card, each should be a string
        #need to be valid suit or value for a card
class Card():
    #String version of suit
    ss = ""
    #String version of value
    vs = ""
    #int version of suit
    suit  = 0
    #int version of value
    value = 0

    #method for initalizing a card with 2 input variables
    def __init__(self, v, s):
        self.setSuit(s)
        self.setValue(v)

    def __str__(self):
        return "(Suit: %s, Value: %s)" % (self.ss, self.vs)

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    #sets int for suit based on inputted string version of suit
    def setSuit(self, s):
        match s.lower():
            case "club" | "0":
                self.suit = 1
                self.ss = "club"
            case "diamond" | "3":
                self.suit = 2
                self.ss = "diamond"
            case "heart" | "1":
                self.suit = 3
                self.ss = "heart"
            case "spade" | "2":
                self.suit = 4
                self.ss = "spade"

    #sets int for value based on inputted string version of value
    def setValue(self, v):

        match v.lower():
            case "a" | "1":
                self.value = 1
                self.vs = "a"
            case "j" | "11":
                self.value = 11
                self.vs = "j"
            case "q" | "12":
                self.value = 12
                self.vs = "q"
            case "k" | "13":
                self.value = 13
                self.vs = "k"
            case default:
                self.value = int(v)
                self.vs = v

#test functions for each method - result in output to console
'''addCard( "2", "spade")
addCard( "A", "Diamond")
getHand()
addCard("J", "heArt")
addCard("2", "Spade")
addCard("10", "club")
getHand()

addCard("7", "Spade")
addCard("14", "heart")

getHand()
print(len(NaoHand))

removeCard("2", "Spade")
getHand()
'''
