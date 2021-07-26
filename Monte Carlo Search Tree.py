from BlackJack import Player
from copy import deepcopy


class Node:
    def __init__(self, state, is_player):
        self.win_count = 0
        self.game_count = 0
        self.state = deepcopy(state)
        self.child_stay = None
        self.child_hit = None
        self.child_DD_hit = None
        self.is_player = is_player

    def simulate(self):
        if self.child_stay is None:
            newstate = deepcopy(self.state)
            if self.is_player:
                self.child_stay = Node(newstate, False)
            else:
                ...

        if self.child_hit is None:
            newstate = deepcopy(self.state)
            newstate.player.hand.addCard(newstate.deck.draw())
            if not newstate.player.has_busted:
                ...
            elif self.is_player:
                self.child_stay = Node(newstate, False)
            else:
                ...
