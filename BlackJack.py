from itertools import product
import random
from typing import ForwardRef
from enum import Enum

SUITS = ['D','C','S','H']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
class VictoryStatus:
    WIN = 1
    TIE = 3
    LOSE = 2

def humanAI(player):
    print(player.hand)
    choice = input('Would you like to hit? ').lower()
    return choice == 'yes'

def simpleAI(player):
    return player.hand.score() < 17


class Player:
    def __init__(self, name, money, AImethod):
        self.name = name
        self.money = money
        self.hand = Hand()
        self.decide_hit = AImethod.__get__(self)


    def has_busted(self):
        return self.hand.score() > 21

    def has_blackjack(self):
        return self.hand.score() == 21


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

class Dealer(Player):
    ...
       

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
    def __init__(self,player,dealer,money):
        self.player = player
        self.deck = Deck()
        self.money = money
        self.dealer = dealer
        self.ended = False

    def play(self):
        self.deck.shuffle()
        self.player.hand.reset_hand()
        self.dealer.hand.reset_hand()
        self.playturn(self.player)
        print('You stay it\'s the dealers turn')
        if not self.ended:
            self.playturn(self.dealer)

    

    def playturn(self,player):   
        for i in range(2):
            player.hand.addCard(self.deck.draw())
        while True:
            if player.has_blackjack():
                print("BlackJack!")
                self.ended = True
                return

            if player.has_busted():
                self.ended = True
                return

            if not player.decide_hit():
                break
            player.hand.addCard(self.deck.draw())          
        
        

    
    def update_money(self):
        status = self.compare()
        if status == VictoryStatus.WIN:
            self.money.win()
        elif status == VictoryStatus.LOSE:
            self.money.bust()
        elif status == VictoryStatus.TIE:
            self.money.tie()

    def compare(self):
        if self.player.has_blackjack():
            return VictoryStatus.WIN
        if self.dealer.has_blackjack():
            return VictoryStatus.LOSE
        if self.player.has_busted():
            return VictoryStatus.LOSE
        if self.dealer.has_busted():
            return VictoryStatus.WIN

        if self.player.hand.score() > self.dealer.score():
            print('You Win!')
            return VictoryStatus.WIN
        elif self.player.hand.score() == self.dealer.hand.score():
            print('Tie game')
            return VictoryStatus.TIE
        elif self.player.hand.score() < self.dealer.hand.score():
            print('You Lose.')
            return VictoryStatus.LOSE

class Statistics:
    def __init__(self):
        self.wins = 0
        self.loses = 0
        self.ties = 0
        self.busts = 0
        self.blackjacks = 0

    def __repr__(self):
        return f"< Wins {self.wins}, Loses {self.loses}, Ties {self.ties}, Busts {self.busts}, BlackJacks {self.blackjacks} >"

class Simulation:
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.playerstats = Statistics()
        self.dealerstats = Statistics()
    
    def run(self, games):
        for _ in range(games):
            game = Game(self.player,self.dealer, 1000)
            game.play()
            compare = game.compare()

            if compare == VictoryStatus.WIN:
                self.playerstats.wins += 1
                self.dealerstats.loses += 1
            elif compare == VictoryStatus.LOSE:
                self.playerstats.loses += 1
                self.dealerstats.wins += 1
            elif compare == VictoryStatus.TIE:
                self.playerstats.ties += 1
                self.dealerstats.ties += 1
            
            if self.player.has_busted():
                self.playerstats.busts += 1
            if self.dealer.has_busted():
                self.dealerstats.busts += 1

            if self.player.has_blackjack():
                self.playerstats.blackjacks += 1
            if self.dealer.has_blackjack():
                self.dealerstats.blackjacks += 1    
            
            


            
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

    def __repr__(self):
        return f"< Hand, Score: {self.score()}, Cards: {self.cards} > "

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

    
        
            























