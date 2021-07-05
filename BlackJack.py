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

class HumanAI:
    def hit(self, player):
        print(player.hand)
        choice = input('Would you like to hit? ').lower()
        return choice == 'yes'

    def bet(self, player):
        try:
            bet = int(input('How much will you bet? '))
            if bet == player.balance:
                print('All in.')
            if bet <= player.balance:
                print('${} is the pot'.format(bet))
                return bet
        except ValueError:
            print('Please use a number')
            self.bet(player)
    
    def double_down(self, player):
        ...

class SimpleAI:
    def hit(self, player):
        return player.hand.score() < 17

    def bet(self, player):
        return 50

    def double_down(self, player):
        return False


class Player:
    def __init__(self, name, balance, AIclass):
        self.name = name
        self._balance = balance
        self.hand = Hand()
        self.decide = AIclass()
        self.bet = 0


    def has_busted(self):
        return self.hand.score() > 21

    def has_blackjack(self):
        return self.hand.score() == 21 and len(self.hand.cards) == 2

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value
        print('You now have ${}'.format(self.balance))

    def prompt(self):
        ask = input('Will you play again? ')
        if ask == 'Y':
            return True

class Dealer(Player):
    def __init__(self, name, AIclass):
        self.name = name
        self.decide = AIclass()
        self.hand = Hand()
            
       
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

class Game:
    def __init__(self,player,dealer):
        self.player = player
        self.deck = Deck()
        self.pot = Pot(self.player)
        self.dealer = dealer

    def play(self):
        self.player.hand = Hand()
        self.dealer.hand = Hand()
        self.pot.collect_bets()
        self.playturn(self.player)
        if not self.ended:
            self.playturn(self.dealer)
        status = self.compare()
        self.pot.settle(status)

    def playturn(self,player):   
        for i in range(2):
            player.hand.addCard(self.deck.draw())
        
        if player.has_blackjack():
            print("BlackJack!")
            return

        while True:
            if player.has_busted():
                return

            if not player.decide.hit():
                print('You stay it\'s the dealers turn')
                return
            
            if player != self.dealer and self.pot.prompt_double_down():
                player.hand.addCard(self.deck.draw())
                return

            player.hand.addCard(self.deck.draw())

    @property     
    def ended(self):
        return self.player.has_busted() or self.player.has_blackjack()

    def compare(self):
        if self.player.has_blackjack():
            print('BlackJack!')
            return VictoryStatus.WIN
        if self.dealer.has_blackjack():
            print('Dealer BlackJack!')
            return VictoryStatus.LOSE
        if self.player.has_busted():
            print('Bust')
            return VictoryStatus.LOSE
        if self.dealer.has_busted():
            print('Dealer has busted you win!')
            return VictoryStatus.WIN

        if self.player.hand.score() > self.dealer.hand.score():
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

    #keep a list of touples

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
            game = Game(self.player,self.dealer)
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
    

class Pot:
    def __init__(self, player):
        self.player = player
        self.doubled_down = False
    
    def collect_bets(self):
        bet = None
        while bet is None or not 0 <= bet <= self.player.balance:
            bet = self.player.decide.bet()

        if bet == self.player.balance:
            print("All in")
        self.player.balance -= bet
        self.player.bet = bet

    @property
    def pot_amount(self):
        return self.player.bet * 2

    def prompt_double_down(self):
        if self.player.balance < self.player.bet:
            return False
        if self.player.decide.double_down():
            self.player.balance -= self.player.bet
            self.player.bet *= 2
            self.doubled_down = True
        return self.doubled_down

    def settle(self, status):
        if status == VictoryStatus.WIN:
            if self.player.has_blackjack():
                self.player.bet *= 1.5
            self.player.balance += self.pot_amount
        elif status == VictoryStatus.TIE:
            self.player.balance += self.player.bet

def Main():
    name = input('What is your name? ') 

    if input('Will you be playing? ') == 'Y':
        choice = HumanAI
    else:
        choice = SimpleAI

    try:
        money = int(input('How much money will you be playing with? Default $100. '))
    except ValueError:
        money = 100

    player = Player(name, money, choice)
    manage = Pot(player)
    dealer = Dealer('Dealer', SimpleAI)
    game = Game(player, dealer, manage)
    manage.Bet()
    game.play()
    
    while player.prompt() and player.balance > 0:
        game = Game(player,dealer,manage)
        manage.Bet()
        game.play()
    
    print(f'Thank you for playing, {player.name}!')
    print(f'You leave with ${player.money}')

player = Player('Sim', 10000, SimpleAI)
dealer = Dealer('Dealer', SimpleAI)   
sim = Simulation(player,dealer)
sim.run(10)
print(sim.playerstats)
'''
Main()
'''