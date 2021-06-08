from itertools import product
import random
from typing import ForwardRef

SUITS = ['D','C','S','H']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Player:
    def __init__(self, name, money, dealer = False):
        self.name = name
        self.money = money
        self.dealer = dealer

    def get_money(self):
        return self.money

    def take_pot(self, pot):
        self.money += pot
        print('You now have ${}'.format(self.money))

    def lose(self, pot):
        self.money -= pot
        print('You now have ${}'.format(self.money))

    def bet(self, bet):
        if bet == self.money:
            self.money = 0
            print("All in")
        else:
            self.money -= bet
            print("you have ${} left".format(self.money))

    def double_down(self, bet): #for when the player wants to double bet and bet it all on the next card to be the winner
        if bet * 2 >= self.money:
            self.money = 0
        else:
            self.money -= bet * 2

    def prompt(self):
        ask = input('Will you play again? ')
        if ask == 'Y':
            return True

    def prompt_hit(self):
        ask = input('Do you want to hit? ')
        if ask == 'Y':
            return True


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

    def __str__(self):
        return self.suit + '_' + self.value


class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:  #creates the cards for the deck
            for v in VALUES:
                card = Card(s,v,False)
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

class Game:
    def __init__(self,player,money):
        self.player = player
        self.deck = Deck()
        self.money = money
        self.hand = Hand()
        self.dealer = Hand()

    def play(self):
        self.deck.shuffle()
        for i in range(2):
            self.hand.addCard(self.deck.draw())
        
        if self.has_blackjack():
            print("BlackJack!")
            self.money.BlackJack()
            return

        while self.hand.score() <= 21 and self.player.prompt_hit():
            self.hand.addCard(self.deck.draw())
            
        if self.hand.score() > 21:
            self.has_busted()
            return
            
        print('You stay it\'s the dealers turn')
        Dealer()
        self.compare()

    def has_blackjack(self):
        return self.hand.score() == 21

    def has_busted(self):
        print('Bust')
        self.money.bust()

    def compare(self):
        if self.hand.score() > self.dealer.score():
            print('You Win!')
            self.money.win()
            self.hand.reset_hand()
            self.dealer.reset_hand()
        elif self.hand.score() == self.dealer.score():
            print('Tie game')
            self.money.tie()
            self.hand.reset_hand()
            self.dealer.reset_hand()
        else:
            print('You Lose.')
            self.money.bust()
            self.hand.reset_hand()
            self.dealer.reset_hand()
            
class Hand:
    def __init__(self):
        self.cards = []
        self.total = 0

    def addCard(self, card):
        self.cards.append(card)
        self.total += 1
        print('Card {}: {} of {}'.format(self.total, card.get_value(), card.get_suit()))

    def reset_hand(self):
        self.cards = []
        self.total = 0

    
    def score(self): #Calculates largest evaluation of the hand that is less than 21
        
        cardsValues = [card.get_values() for card in self.cards]
        possibilities = product(*cardsValues)
        valedValues = []
        badValues = []
        
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
    

class Money:
    def __init__(self, money, player):
        self.money = money
        self.pot = 0
        self.player = player

    def Bet(self):
        try:
            bet = int(input('How much will you bet? '))
            if bet == self.player.get_money():
                print('All in.')
            if bet <= self.player.get_money():
                self.pot += bet
                print('${} is the pot'.format(self.pot))
                return self.pot    
            else:
                print('You do not have enough to bet that much')
                self.Bet()
        except ValueError:
            print('Please use a number')
            self.Bet()

    def BlackJack(self):
        self.pot *= 1.5
        self.player.take_pot(self.pot)
        self.pot = 0

    def bust(self):
        self.player.lose(self.pot)
        self.pot = 0

    def win(self):
        self.player.take_pot(self.pot)
        self.pot = 0
    
    def tie(self):
        self.pot = 0

def Main():
    name = input('What is your name? ')
    try:
        money = int(input('How much money will you be playing with? Default $100. '))
    except ValueError:
        money = 100
    player = Player(name, money)
    manage = Money(money,player)
    dealer = Player('Dealer', 0, True)
    game = Game(player,manage)
    manage.Bet()
    game.play()
    while player.prompt() and player.get_money() > 0:
        game = Game(player,manage)
        manage.Bet()
        game.play()
    
    print('Thank you for playing, {}!'.format(player.name))
    print('You leave with ${}'.format(player.get_money()))
    

Main()

    
        
            























