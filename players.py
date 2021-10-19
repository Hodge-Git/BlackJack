from BlackJack import Hand, VictoryStatus
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
