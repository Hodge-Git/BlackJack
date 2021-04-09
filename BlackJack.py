import random

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

    def start_hand(self, deck):  #Starts the hand by drawing 2 cards, but it only draws last card created from for loop and copies it
        for i in range(2):
            card = deck.draw()
            print('Card {}: {} of {}'.format(i+1, card.get_value(), card.get_suit()))
            self.hand.append(card)
            
        for i in self.hand:
            if (i.get_value() == 'J') or (i.get_value() == 'Q') or (i.get_value() == 'K'):
                self.total += 10
            elif (i.get_value() == 'A') and self.total <= 10:
                self.total += 11
            elif (i.get_value() == 'A') and self.total < 10:
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
        elif (card.get_value() == 'A') and self.total < 10:
            self.total += 1
        else:
            self.total += int(card.get_value())
        return self.total

    def stand(self):
        self.stand = True

    def bet(self, bet):
        if bet > self.money:
            print("You do not have enough to bet that much")
            self.overBet = True
            return self.overBet
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

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def __str__(self):
        return self.suit + '_' + self.value


class Deck:
    def __init__(self):
        self.deck = []

    def add_card(self, card):
        self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)
        #print('Deck:', [str(c) for c in self.deck])
        return self.deck

    def draw(self):
        return self.deck.pop()

    def recall(self, player_hand, dealer_hand):
        for i in player_hand:
            self.deck.append(player_hand.pop())

        for i in dealer_hand:
            self.deck.append(dealer_hand.pop())
    def get_card(self, suit, value):
        for c in self.deck:
            if (c.get_suit == suit) and (c.get_value == value):
                return c

suits = ['D','C','S','H']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

deck = Deck()
for s in suits:  #creates the cards for the deck
    for v in values:
        card = Card(s,v)
        #print(card)
        deck.add_card(card)
pot = 0
play = True #is the check variable for ending the game

name = input('What is your name? ')
money = int(input('How much money will you be playing with? Default $100. '))
player = Player(name, money)
dealer = Player('Dealer', 0, True)

'''
deck.shuffle()
for _ in range(5):
    card = deck.draw()
    print('{} of {}'.format(card.get_value(), card.get_suit()))
'''

while (play == True) or (player.get_money > 0):
    deck.shuffle()
    try:
        bet = int(input('how much will you bet? '))
        player.bet(bet)
        if player.overBet == True:
            continue
        else:
            pot += bet
            print('{} is the pot'.format(pot))
            player.start_hand(deck)
            if player.get_total() == 21:
                print('BlackJack!')
                deck.recall(player.hand,dealer.hand)
                player.take_pot(pot * 1.5)
                pot = 0
            else:
                while player.stand == False:
                    hit = input('do you want to hit? ')
                    if hit == 'Y':
                        player.hit(deck)
                        if player.get_total() > 21:
                            print('Bust')    
                    else:
                        player.stand()
                        print('You stay, Dealers turn.')
                        
    except ValueError:
        print('Please use a number.')
        continue
    
    
        
            























