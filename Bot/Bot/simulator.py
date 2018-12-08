#!/usr/bin/python
# Ported from the hackman python2 starter package

import sys
import traceback
import random
import time
import copy
import timeit

from . import board
from . import player
from . import minimax
from . import state

Mapper = {0:"1", 1:"2", 2:".", 3:"*"}
PLAYER1, PLAYER2, EMPTY, BLOCKED = [0, 1, 2, 3]
class Game():
    def __init__(self):
        self.initial_timebank = 0
        self.time_per_move = 10
        self.player_names = []
        self.my_bot = "not set"
        self.my_botid = 0
        self.other_botid = 1
        self.field_width = 8
        self.field_height = 8

        self.field = None
        self.round = 0
        self.last_update = 0
        self.last_timebank = 0
        self.players = [player.Player(), player.Player()]

        self.current_state = None
        self.previous_state = None

    def my_player(self):
        return self.players[self.my_botid]

    def other_player(self):
        return self.players[self.other_botid]

    def update_field(self, move1, move2):
        """
        update the field board of the game
        :param move1: move of player1 ((row,col), string)
        :param move2: move of player2 ((row,col), string)
        :return:
        """
        if not move1 or not move2:
            #game ended
            return
        p1_r, p1_c = self.current_state.players[0].row, self.current_state.players[0].col
        p2_r, p2_c = self.current_state.players[1].row, self.current_state.players[1].col
        self.current_state.board.cell[p1_r][p1_c]=BLOCKED
        self.current_state.board.cell[p2_r][p2_c]=BLOCKED
        self.current_state.board.cell[p1_r + move1[0][0]][p1_c + move1[0][1]]=PLAYER1
        self.current_state.board.cell[p2_r + move2[0][0]][p2_c + move2[0][1]]=PLAYER2

    def update_players(self, move1, move2):
        """
        update the player positions
        :param move1: move of player1 ((row,col), string)
        :param move2: move of player2 ((row,col), string)
        :return:
        """
        if not move1 or not move2:
            #game ended
            return
        self.current_state.players[0].row += move1[0][0]
        self.current_state.players[0].col += move1[0][1]
        self.current_state.players[1].row += move2[0][0]
        self.current_state.players[1].col += move2[0][1]

    def checkWin(self):
        """
        check if the game has a win or draw
        :param move1: move of player1 ((row,col), string)
        :param move2: move of player2 ((row,col), string)
        :return: whether the game has ended
        """
        if self.current_state.players[0].row == self.current_state.players[1].row and self.current_state.players[0].col == self.current_state.players[1].col:
            print("it's a draw1")
            return 3
        win = 0
        move1 = self.current_state.board.legal_moves(0, self.players)
        move2 = self.current_state.board.legal_moves(1, self.players)
        if not move2:
            win += 1
        if not move1:
            win += 2
        if win == 1:
            print("winner player 1")
        elif win == 2:
            print("winner player 2")
        elif win == 3:
            print("it's a draw2")
        return win

    def initialize(self):
        'parse input, update game state and call the bot classes do_turn method'
        self.field = board.Board(self.field_width, self.field_height)
        row = random.choice(range(self.field_height))
        col = random.choice(range(self.field_width))
        self.players[0].row = row
        self.players[0].col = col
        self.players[1].row = row
        self.players[1].col = self.field_width - 1 - col
        self.field.cell[row][col]=PLAYER1
        self.field.cell[row][self.field_width - 1 - col]=PLAYER2
        self.current_state = state.State(self)

    def run(self, bot, bot2):
        '''
        parse input, update game state and call the bot classes do_turn method'
        '''
        not_finished = True
        self.initialize()
        self.current_state.board.output()
        while(not_finished):
            print("========================================")
            if True:
                if True:
                    if (bot.game == None):
                        bot.setup(self)
                        bot2.setup(self)
                    start1 = timeit.default_timer()
                    move1 = bot.do_turn(minimax.MinimaxAgent(evalFunc = minimax.attackAndBlockEvalFunc, depth = 4))
                    end1 = timeit.default_timer()

                    start2 = timeit.default_timer()
                    move2 = bot2.do_turn(minimax.AlphaBetaAgent(evalFunc = minimax.maxDirEvalFunc, depth = 4), True)
                    end2 = timeit.default_timer()
                    #update fields
                    self.update_field(move1, move2)
                    #update player positions
                    self.update_players(move1, move2)
                    #check if game ended
                    
                    not_finished = not self.checkWin()
                    
                    self.current_state.board.output()
                print("========================================")
                
                #print end1 - start1, end2 - start2
                time.sleep(1)