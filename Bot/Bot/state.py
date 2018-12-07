#!/usr/bin/python
# This file defines the state of the search algorithm

import sys
import traceback
import random
import time
import copy

from . import board
from . import player
from . import game

class State:
    '''
    Game state: board information and player positions
    '''
    def __init__(self, game):
        self.board = game.field
        self.players = game.players

    def getNextPlayer(self, agent):
        return agent ^ 1

    def getLegalActions(self, agent):
        return self.board.legal_moves(agent, self.players)

    def isEnd(self, agent):
        agt_nxt_len = len(self.getLegalActions(agent))
        opp_nxt_len = len(self.getLegalActions(self.getNextPlayer(agent)))
        if agt_nxt_len != 0 and opp_nxt_len != 0:
            return 0 # not end of game
        if agt_nxt_len == 0 and opp_nxt_len == 0:
            return 2 # is a draw
        if agt_nxt_len != 0:
            return 1 # agent win the game
        return -1 # enemy win the game

    def getMyReward(self, agent):
        e = self.isEnd(agent)
        if e == 0:
            return 0
        if e == 2:
            return 10000
        if e == 1:
            return 50000
        return -50000

    def generateSuccessor(self, agent, action):
        '''
        Generate successor of a state based on agent and action
        '''
        agt_legal_actions = self.getLegalActions(agent)
        if action not in agt_legal_actions:
            raise Exception('Cannot generate successor: illegal action')

        # Deep copy current state
        nxt_state = copy.deepcopy(self)
        old_row, old_col = self.players[agent].row, self.players[agent].col
        new_row = old_row + action[0][0]
        new_col = old_col + action[0][1]
        nxt_state.board.update_cell(old_row, old_col, 3) # block the old cell
        nxt_state.board.update_cell(new_row, new_col, agent) # update the head of the old cell
        nxt_state.players[agent].row = new_row
        nxt_state.players[agent].col = new_col
        return nxt_state


        