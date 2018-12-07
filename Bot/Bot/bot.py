import random
import sys
from . import minimax
from .import state
class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def calculate_score(self, id, players, move):
        #move is ((delta_row, delta_col), direction string)
        my_player = players[id]
        row = my_player.row
        col = my_player.col
        dir = move[0]
        iter = 15
        count = 0
        while (self.game.field.in_bounds(row, col) and count < iter):
            row += dir[0]
            col += dir[1]
            if not self.game.field.is_legal(row, col, id):
                break
            count += 1
        exploreDir =[ (-dir[1], -dir[0]), (dir[1], dir[0])]
        counts = [None, None]
        minSum = -1
        mid = count // 2
        for i in range(mid, count):
            row = my_player.row + dir[0]*i
            col = my_player.col + dir[1]*i
            sumCounter = 0
            cnt = []
            for direction in exploreDir:
                counter = 0
                row += direction[0]
                col += direction[1]
                while (self.game.field.in_bounds(row, col) and counter < iter):
                    row += dir[0]
                    col += dir[1]
                    if not self.game.field.is_legal(row, col, id):
                        break
                    counter += 1
                sumCounter += counter
                cnt.append(counter)
                row = my_player.row + dir[0] * i
                col = my_player.col + dir[1] * i
            if sumCounter > minSum:
                counts = cnt
                minSum = sumCounter
        weight1 = 8
        weight2 = 5
        weight3 = 5
        return weight1*count + weight2*counts[0] + weight3*counts[1]

    def do_turn(self, mmAgent = minimax.MinimaxAgent(), other = False):
        #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #self.game.field.output()
        #if other:
            #print"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if not other:
            legal = self.game.field.legal_moves(0, self.game.players)
        else:
            legal = self.game.field.legal_moves(1, self.game.players)
        if len(legal) == 0:
            self.game.issue_order_pass()
            return None
        else:
            #
            chosen = None
            bestScore = 0
            #print("legal from bot:", legal)
            gameState = state.State(self.game)
            if not other:
                chosen = mmAgent.getAction(self.game.my_botid,gameState)
            else:
                chosen = mmAgent.getAction(self.game.other_botid, gameState)
            """
            if other:
                chosen = random.choice(legal)
            else:
                for move in legal:
                    if not other:
                        score = self.calculate_score(self.game.my_botid, self.game.players, move)
                    else:
                        score = self.calculate_score(self.game.other_botid, self.game.players, move)
                    if score > bestScore:
                        chosen = move
                        bestScore = score
            if not other:
                self.game.issue_order(chosen)
            else:
                self.game.issue_order(chosen, self.game.other_botid)
            return chosen
        """
        return chosen
