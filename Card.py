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

    def __hash__(self):
        uid = str(self.suit) + ":" + str(self.value)
        return hash(uid)

    def __repr__(self):
        return "(Suit: %s, Value: %s)" % (self.ss, self.vs)
    
    def cardName(self):
        value = self.vs
        suit = self.ss + "s"
        if value == "a":
            value = "ace"
        elif value == "q":
            value = "queen"
        elif value == "j":
            value = "jack"
        elif value == "k":
            value = "king"
        
        return "%s of %s" % (value, suit)

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    #sets int for suit based on inputted string version of suit
    def setSuit(self, s):
        s = s.lower()
        if s == "club" or s == "0":
            self.suit = 1
            self.ss = "club"
        elif s == "diamond" or s == "3":
            self.suit = 2
            self.ss = "diamond"
        elif s == "heart" or s == "1":
            self.suit = 3
            self.ss = "heart"
        elif s == "spade" or s == "2":
            self.suit = 4
            self.ss = "spade"

    def setValue(self, v):
        self.vs = v.lower()
        #sets string value to lowercase
        v = v.lower()

        #sets int for value based on inputted string version of value
        if v == "a" or v == "1":
            self.value = 1
            self.vs = "a"
            self.value = 10
        elif v == "j" or v == "11":
            self.value = 11
            self.vs = "j"
        elif v == "q" or v == "12":
            self.value = 12
            self.vs = "q"
        elif v == "k" or v == "13":
            self.value = 13
            self.vs = "k"
        else:
            self.value = int(v)
            self.vs = v
