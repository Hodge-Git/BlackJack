from itertools import product
import random
from typing import ForwardRef

class Player:
    def __init__(self, name, money = 100, dealer = False):
        self.name = name
        self.money = money
        self.hand = []
        self.stand = False
        self.dealer = dealer
        self.overBet = False
        self.total = 0

    def get_money(self):
        return self.money

    def get_total(self):
        return self.total

    def take_pot(self, pot):
        self.money += pot
        print('You now have ${}'.format(self.money))

    def lose(self, pot):
        self.money -= pot
        print('You now have ${}'.format(self.money))

    def resetTotal(self):
        self.total = 0

    def start_hand(self, deck):
        for i in range(2):
            card = deck.draw()
            print('Card {}: {} of {}'.format(i+1, card.get_value(), card.get_suit()))
            self.hand.append(card)
            
        for i in self.hand:
            if (i.get_value() == 'J') or (i.get_value() == 'Q') or (i.get_value() == 'K'):
                self.total += 10
            elif (i.get_value() == 'A') and self.total >= 10:
                self.total += 11
            elif (i.get_value() == 'A'):
                self.total += 1
            else:
                self.total += int(i.get_value())
        return self.total

    def hit(self, deck):
        card = deck.draw()
        print('Card {}: {} of {}'.format(int(len(self.hand) + 1),card.get_value(), card.get_suit()))
        self.hand.append(card)
        if (card.get_value() == 'J') or (card.get_value() == 'Q') or (card.get_value() == 'K'):
            self.total += 10
        elif (card.get_value() == 'A') and self.total >= 10:
            self.total += 11
        elif (card.get_value() == 'A'):
            self.total += 1
        else:
            self.total += int(card.get_value())
        
        for x in self.hand: #changes Ace value in hand if over 21
            if x.get_value() == "A" and self.total > 21 and x.usedAce == False:
                self.total -= 10
                x.use_ace()
        return self.total

    def Stand(self):
        self.stand = True

    def bet(self, bet):
        if bet > self.money:
            print("You do not have enough to bet that much")
            return False
        elif bet == self.money:
            self.money = 0
            print("All in")
        else:
            self.money -= bet
            print("you have {} left".format(self.money))

    def double_down(self, bet): #for when the player wants to double bet and bet it all on the next card to be the winner
        if bet * 2 >= self.money:
            self.money = 0
        else:
            self.money -= bet * 2

    def prompt(self):
        ask = input('Will you play again? ')
        if ask == 'Y':
            return True


class Card:
    def __init__(self, suit, value, usedAce = False):
        self.suit = suit
        self.value = value
        self.usedAce = usedAce

    def use_ace(self):
        self.usedAce = True

    def get_values(self):
        if self.value in ['J','K','Q']:
            return [10]
        if self.value == 'A':
            return [1,11]
        return [int(self.value)]


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

    def recall(self, player_hand, dealer_hand = ()): #possibly get rid of
        for i in player_hand:
            self.deck.append(player_hand.pop())

        for i in dealer_hand:
            self.deck.append(dealer_hand.pop())

    def get_card(self, suit, value):
        for c in self.deck:
            if (c.get_suit == suit) and (c.get_value == value):
                return c

SUITS = ['D','C','S','H']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

deck = Deck()
for s in SUITS:  #creates the cards for the deck
    for v in VALUES:
        card = Card(s,v,False)
        deck.add_card(card)

for s,v in product(SUITS,VALUES):
    ...

name = input('What is your name? ')
money = int(input('How much money will you be playing with? Default $100. '))
player = Player(name, money)
dealer = Player('Dealer', 0, True)

class Game:
    def __init__(self,player):
        self.player = player
        self.deck = Deck()

    def play(self):
        self.deck.shuffle()
        player.start_hand()
        if self.has_blackjack():
            print("BlackJack!")
            money.BlackJack()
            return

        while player.get_hand_value() <= 21 and player.prompt_hit():
            player.hit
            
        if player.get_hand_value() > 21:
            self.has_busted()
            return

        if not player.prompt_hit():
            player.stand()
            print('You stay it\'s the dealers turn')
            Dealer()

        self.compare()

    def has_blackjack(self):
        return player.get_hand_value() == 21

    def has_busted(self):
        print('Bust')
        Money.bust()

    def compare(self):
        if player.get_hand_value() > dealer.get_hand_value():
            print('You Win!')
            Money.win()
            player.resetTotal()
        elif player.get_hand_value() == dealer.get_hand_value():
            print('Tie game')
            Money.tie()
            player.resetTotal()
        else:
            print('You Lose.')
            Money.bust()
            player.resetTotal()
        
        
        
        
        
        
        
        
        turn = 0
        pot = 0
        play = True #is the check variable for ending the game
        while play == True and player.get_money() >= 0:
            turn += 1
            deck.shuffle()
            BlackJack = False
            Bust = False
            Betting(pot)
            player.start_hand(deck)
            if player.get_total() == 21: #this is for a BlackJack
                print('BlackJack!')
                BlackJack = True
                potManage(pot, Bust, BlackJack)
                deck.recall(player.hand,dealer.hand)
            else:
                while player.stand == False or Bust == False:
                    hit = input('do you want to hit? ')
                    if hit == 'Y':
                        player.hit(deck)
                        if player.get_total() > 21: #This is for busting
                            print('Bust')
                            Bust = True
                            Deck.recall(player.hand,dealer.hand)
                            potManage(pot, Bust, BlackJack)
                            player.resetTotal()
                            turn = 0
                            playCheck = input('Do you want to play again? ')
                            if playCheck == "N":
                                play = False
                                break
                            else:
                                player.Stand()
                                print('You stay it\'s the dealers turn')
                                Dealer()
    
    print('Thank you for playing!')

            
class Hand:
    def __init__(self):
        self.cards = []
        

    def addCard(self, card):
        self.cards.append(card)
    
    def score(self): #Calculates largest evaluation of the hand that is less than 21
        
        cardsValues = [card.get_values() for card in self.cards]
        possibilities = product(*cardsValues)
        handValues = []
        for possibility in possibilities:
            handScore = sum(possibility)
            if handScore <= 21:
                handValues.append(handScore)
        return max(handValues)
    

class Money:
    def __init__(self, money):
        self.money = money
        self.pot = 0

    def Bet(self):
        try:
            bet = int(input('How much will you bet? '))
            if player.bet(bet):
                self.pot += bet
                print('{} is the pot'.format(self.pot))
                return self.pot        
            else:
                self.Bet()
        except ValueError:
            print('Please use a number')
            self.Bet()

    def BlackJack(self):
        self.pot *= 1.5
        player.take_pot(self.pot)
        self.pot = 0

    def bust(self):
        player.lose(self.pot)
        self.pot = 0


    def win(self):
        player.take_pot(self.pot)
        self.pot = 0
    
    def tie(self):
        self.pot = 0
        

def Main():
    name = input('What is your name? ')
    money = int(input('How much money will you be playing with? Default $100. '))
    player = Player(name, money)
    manage = Money(money)
    dealer = Player('Dealer', 0, True)
    while player.prompt() and player.get_money() > 0:
        manage.Bet()
        game = Game(player)
        game.play()
    
    print('Thank you for playing!')
    

    

    

Main()

    
        
            























