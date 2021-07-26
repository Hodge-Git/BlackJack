from itertools import product
import random
from typing import ForwardRef
from enum import Enum
from pprint import pformat

SUITS = ['D','C','S','H']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
class VictoryStatus:
    WIN = 1
    TIE = 3
    LOSE = 2

def flip_victory_status(status):
    if status == VictoryStatus.WIN:
        return VictoryStatus.LOSE
    if status == VictoryStatus.LOSE:
        return VictoryStatus.WIN
    return status

def victory_to_str(status):
    if status == VictoryStatus.WIN:
        return "Win"
    if status == VictoryStatus.LOSE:
        return "Lose"
    if status == VictoryStatus.TIE:    
        return "Tie"

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

    @property
    def has_busted(self):
        return self.hand.score() > 21

    @property
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
        status = self.outcome
        self.pot.settle(status)

    def playturn(self,player):   
        for i in range(2):
            player.hand.addCard(self.deck.draw())
        
        if player.has_blackjack:
            print("BlackJack!")
            return

        while True:
            if player.has_busted:
                return

            if not player.decide.hit(self.player):
                print('You stay it\'s the dealers turn')
                return
            
            if player != self.dealer and self.pot.prompt_double_down():
                player.hand.addCard(self.deck.draw())
                return

            player.hand.addCard(self.deck.draw())

    @property     
    def ended(self):
        return self.player.has_busted or self.player.has_blackjack

    @property
    def outcome(self):
        if self.player.has_blackjack:
            print('BlackJack!')
            return VictoryStatus.WIN
        if self.dealer.has_blackjack:
            print('Dealer BlackJack!')
            return VictoryStatus.LOSE
        if self.player.has_busted:
            print('Bust')
            return VictoryStatus.LOSE
        if self.dealer.has_busted:
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
        self.matches = []

    def __repr__(self):
        match_history = pformat(self.matches, width = 120)
        return f"< Match History {match_history} \n Wins {self.win_count}, Loses {self.lose_count}\n Double Downs {self.doubled_down_count}, Double Down Profit {self.profit_from_double_down} >"

    @property
    def win_count(self):
        return sum([1 for match in self.matches if match.outcome == VictoryStatus.WIN])

    @property
    def lose_count(self):
        return sum(match.outcome == VictoryStatus.LOSE for match in self.matches)

    @property
    def doubled_down_count(self):
        return sum(match.doubled_down for match in self.matches)

    @property
    def profit_from_double_down(self):
        profit = 0
        for matches in self.matches:
            if matches.doubled_down:
                if matches.outcome == VictoryStatus.WIN:
                    profit += matches.bet
                if matches.outcome == VictoryStatus.LOSE:
                    profit -= matches.bet
        return profit
    
    @property
    def avg_profit_from_double_down(self):
        return self.profit_from_double_down / self.doubled_down_count    

class MatchStats:
    def __init__(self, bet, outcome, blackjack, bust, doubled_down):
        self.bet = bet
        self.outcome = outcome
        self.blackjack = blackjack
        self.busted = bust
        self.doubled_down = doubled_down
        
    def __repr__(self):
        outcome = victory_to_str(self.outcome)
        return f"< Outcome {outcome}, Bet {self.bet}, Busted {self.busted}, BlackJacked {self.blackjack}, Doubled down {self.doubled_down} >"

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
            playerMatch = MatchStats(self.player.bet, game.outcome, self.player.has_blackjack, self.player.has_busted, game.pot.doubled_down)
            dealerMatch = MatchStats(self.player.bet, flip_victory_status(game.outcome), self.dealer.has_blackjack, self.dealer.has_busted, game.pot.doubled_down) 
            self.playerstats.matches.append(playerMatch)  
            self.dealerstats.matches.append(dealerMatch)
            
class Pot:
    def __init__(self, player):
        self.player = player
        self.doubled_down = False
    
    def collect_bets(self):
        bet = None
        while bet is None or not 0 <= bet <= self.player.balance:
            bet = self.player.decide.bet(self.player)

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
        if self.player.decide.double_down(self.player):
            self.player.balance -= self.player.bet
            self.player.bet *= 2
            self.doubled_down = True
        return self.doubled_down

    def settle(self, status):
        if status == VictoryStatus.WIN:
            if self.player.has_blackjack:
                self.player.bet *= 1.5
                self.player.bet = int(self.player.bet)
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