import random

SUITS = ['D','C','S','H']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_values(self):
        if self.value in ['J','K','Q']:
            return [10]
        if self.value == 'A':
            return [1,11]
        return [int(self.value)]

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def __repr__(self):
        return self.suit + '_' + self.value

class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:  #creates the cards for the deck
            for v in VALUES:
                card = Card(s,v)
                self.add_card(card)
        self.shuffle()

    def add_card(self, card):
        self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)
        return self.deck

    def draw(self):
        return self.deck.pop()

    def get_card(self, suit, value):
        for c in self.deck:
            if (c.get_suit == suit) and (c.get_value == value):
                return c

class Hand:
    def __init__(self):
        self.cards = []
        self.total = 0

    def addCard(self, card):
        self.cards.append(card)
        self.total += 1
        print('Card {}: {} of {}'.format(self.total, card.get_value(), card.get_suit()))

    def __repr__(self):
        return f"< Hand, Score: {self.score()}, Cards: {self.cards} > "

    def score(self): #Calculates largest evaluation of the hand that is less than 21
        cardsValues = [card.get_values() for card in self.cards]
        possibilities = product(*cardsValues)
        valedValues = []
        badValues = []
        
        if not self.cards:
            return 0

        for possibility in possibilities:
            handScore = sum(possibility)
            if handScore <= 21:
                valedValues.append(handScore)
            else:
                badValues.append(handScore)
        
        if valedValues: 
            return max(valedValues)
        else:
            return min(badValues)