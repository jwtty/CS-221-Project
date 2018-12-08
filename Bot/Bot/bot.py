import random
import sys
from . import minimax
from .import state
class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def do_turn(self, mmAgent = minimax.MinimaxAgent(), other = False):
        chosen = None
        bestScore = 0
        #print("legal from bot:", legal)
        gameState = self.game.current_state
        if not other:
            chosen = mmAgent.getAction(self.game.my_botid,gameState)
        else:
            chosen = mmAgent.getAction(self.game.other_botid, gameState)
        return chosen
