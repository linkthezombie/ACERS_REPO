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
"""
#import needed functionality for arrays and classes
#import array 
from array import array
# ab_classes.py

#array to store cards
NaoHand  = []

#adds a new card to the array
#takes string for value and suit to add to the array
def addCard(v, s):
        #checks if new card is a valid card, if yes, create the card
        if checkValidity(v, s) == True:
            c = Card(v, s)
            #checks if the card is already in the hand, if it is, can't add a repeat to the hand
            if findCardInHand(c) == True:
                    print("\nCard already exists in hand")                        
                    return 0
            else:
                print("\nAdding: Suit: "+ s + ", Value: "+ v)
                #check if the card will be the first entry in the array and add
                if len(NaoHand) == 0:
                        NaoHand.append(c)
                #insert at front of the array
                elif greater(NaoHand[0], c) == True:
                        NaoHand.insert(0, c)
                #insert at back of array
                elif greater(NaoHand[len(NaoHand)-1], c) == False:
                        NaoHand.append(c)
                else:
                    #in middle of array, loop through till right location is found
                    i = 0
                    for x in NaoHand:
                        if greater(c, x) == False:
                            NaoHand.insert(i, c)
                            return 0
                        i= i+1
                print("\nAdded to hand")
        else:
            print("\nInvalid card: suit = " + s.lower() + ", value = "+ v.lower())
        return 0


#determine which card is "greater"
#true if c1 is greater, false if c2 is greater
#takes two card objects to compare the value of
#based on suit then face value
def greater(c1, c2):
        #checks if c1's suit is larger than c2's
        if c1.suit > c2.suit:
                return True
        #suits are the same value
        elif c1.suit == c2.suit:
                #checks which face value of the cards is larger
                if c1.value > c2.value:
                        return True
                else:
                        return False
        #c2's suit is of a larger value
        else:
                return False

#remove a card from hand
#takes a string value and suit for the card that should be removed
def removeCard(v, s):
        #check if inputed variables make a valid card
        if checkValidity(v, s) == True:
        #make a card object
            c = Card(v, s)
            #check if the card in the the hand, if it is not, exit because you can't remove something that isn't there
            if findCardInHand(c) == True:
                i = 0
                #loop till card is found in the array
                for x in NaoHand:
                        if x.suit == c.suit and x.value == c.value:
                        #remove the card
                            NaoHand.pop(i)
                            return 0
                        else:
                            i += 1
                print("\nRemoved from hand")
            else:
                print("\nCard isn't in hand")
        else:
            print("\nInvalid card: suit = " + s.lower() + ", value = "+ v.lower())
        return 0

#check for valid input matching a real playing card
#inputed value and suit must match a real suit and value for a playing card
#if it doesn't, program returns false
#takes in a string reprsenting the value and another for the suit
def checkValidity( v, s):
    t = False
#check for a valid value
    if v.lower() == "a" or v.lower() == "2" or v.lower() == "3"  or v.lower() == "4" or v.lower() == "5" or v.lower() == "6" or v.lower() == "7" or v.lower() == "8" or v.lower() == "9" or v.lower() == "10" or v.lower() == "j" or v.lower() == "q" or v.lower() == "k":
            #check for a valid suit
            if s.lower() == "spade" or s.lower() == "club" or s.lower() == "diamond" or s.lower() == "heart":
                #both suit and value are vaild
                    t = True
    return t

#searches for card in array, returns true if found and false if not present in the array
#preconditions - takes in a Card object
def findCardInHand(c):
        t = False
        #for each item in the array, check if the passed in card matches the current card in the array
        #if yes, set variable to True
        for x in NaoHand:
                if x.value == c.value and x.suit == c.suit:
                        t = True
        return t

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
        #sets the strings the the inputed values
            self.ss = s.lower()
            self.vs = v.lower()
        #sets int for suit based on inputted string version of suit
            if s.lower() == "club" or s == "0":
                    self.suit = 1
            elif s.lower() == "diamond" or s == "3":
                    self.suit = 2
            elif s.lower() == "heart" or s == "1":
                    self.suit = 3
            elif s.lower() == "spade" or s == "2":
                self.suit = 4
        #sets string value to lowercase
            v = v.lower()

        #sets int for value based on inputted string version of value
            if v == "a" or v == "1":
                    self.value = 1
            elif v == "2" or v == "2":
                    self.value = 2
            elif v == "3" or v == "3":
                    self.value = 3
            elif v == "4" or v == "4":
                    self.value = 4
            elif v == "5" or v == "5":
                    self.value = 5
            elif v == "6" or v == "6":
                    self.value = 6
            elif v == "7" or v == "7":
                    self.value = 7
            elif v == "8" or v == "8":
                    self.value = 8
            elif v == "9" or v == "9":
                    self.value = 9
            elif v == "10" or v == "10":
                    self.value = 10
            elif v == "j" or v == "11":
                    self.value = 11
            elif v == "q" or v == "12":
                    self.value = 12
            elif v == "k" or v == "13":
                    self.value = 13

        def __str__(self):
               return "(Suit: %s, Value: %s)" % (self.ss, self.vs)
        
        def __eq__(self, other):
               return self.suit == other.suit and self.value == other.value

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

