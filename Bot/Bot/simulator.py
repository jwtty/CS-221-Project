#!/usr/bin/python
# Ported from the hackman python2 starter package

import sys
import traceback
import random
import time

from . import board
from . import player
import time
import timeit
from . import minimax

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

    def my_player(self):
        return self.players[self.my_botid]

    def other_player(self):
        return self.players[self.other_botid]

    def update(self, data):
        'parse input'
        # start timer
        self.last_update = time.time()
        for line in data.split('\n'):
            line = line.strip()
            if len(line) > 0:
                tokens = line.split()
                key0 = tokens[0]
                if key0 == "settings":
                    key1 = tokens[1]
                    if key1 == "timebank":
                        self.timebank = int(tokens[2])
                    if key1 == "time_per_move":
                        self.time_per_move = int(tokens[2])
                    if key1 == "player_names":
                        self.player_names = tokens[2].split(',')
                    if key1 == "your_bot":
                        self.my_bot = tokens[2]
                    if key1 == "your_botid":
                        self.my_botid = int(tokens[2])
                        self.other_botid = 1 - self.my_botid
                    if key1 == "field_width":
                        self.field_width = int(tokens[2])
                    if key1 == "field_height":
                        self.field_height = int(tokens[2])
                elif key0 == "update":
                    key1 = tokens[1]
                    if key1 == "game":
                        key2 = tokens[2]
                        if key2 == "round":
                            self.round = int(tokens[3])
                        elif key2 == "field":
                            if self.field == None:
                                self.field = board.Board(self.field_width, self.field_height)
                            self.field.parse(self.players, tokens[3])
                elif key0 == "action" and tokens[1] == "move":
                    self.last_timebank = int(tokens[2])
                    # Launching bot logic happens after setup finishes
                elif key0 == "quit":
                    pass


    def time_remaining(self):
        return self.last_timebank - int(1000 * (time.clock() - self.last_update))

    def issue_order(self, order, player_id = 0):
        """issue an order, noting that (col, row) is the expected output
        however internally, (row, col) is used."""
        #order is ((delta_row, delta_col), string)
        #self.players[player_id].row + order[0][0]
        #self.players[player_id].col + order[0][1]
        #update field
        return
    def issue_order_pass(self, player_id = 0):
        """ pass the turn """
        return
        sys.stdout.write('pass\n')
        sys.stdout.flush()

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
        p1_r, p1_c = self.players[0].row, self.players[0].col
        p2_r, p2_c = self.players[1].row, self.players[1].col
        self.field.cell[p1_r][p1_c]=BLOCKED
        self.field.cell[p2_r][p2_c]=BLOCKED
        self.field.cell[p1_r + move1[0][0]][p1_c + move1[0][1]]=PLAYER1
        self.field.cell[p2_r + move2[0][0]][p2_c + move2[0][1]]=PLAYER2

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
        self.players[0].row += move1[0][0]
        self.players[0].col += move1[0][1]
        self.players[1].row += move2[0][0]
        self.players[1].col += move2[0][1]

    def checkWin(self):
        """
        check if the game has a win or draw
        :param move1: move of player1 ((row,col), string)
        :param move2: move of player2 ((row,col), string)
        :return: whether the game has ended
        """
        if self.players[0].row == self.players[1].row and self.players[0].col == self.players[1].col:
            print("it's a draw1")
            return False
        win = 0
        move1 = self.field.legal_moves(0, self.players)
        move2 = self.field.legal_moves(1, self.players)
        if not move2:
            win += 1
        if not move1:
            win += 2
        if win == 1:
            print("winner player 1")
            return False
        elif win == 2:
            print("winner player 2")
            return False
        elif win == 3:
            print("it's a draw2")
            return False
        return True

    def run(self, bot, bot2):
        '''
        parse input, update game state and call the bot classes do_turn method'
        '''
        not_finished = True
        self.field = board.Board(self.field_width, self.field_height)
        row = random.choice(range(self.field_height))
        col = random.choice(range(self.field_width))
        self.players[0].row = row
        self.players[0].col = col
        self.players[1].row = row
        self.players[1].col = self.field_width - 1 - col
        self.field.cell[row][col]==PLAYER1
        self.field.cell[row][self.field_width - 1 - col]==PLAYER2
        field = ""
        for row in range(self.field_height):
            for col in range(self.field_width):
                if 0 == self.field.cell[row][col]:
                    field += Mapper[0]
                elif 1 == self.field.cell[row][col]:
                    field += Mapper[1]
                else:
                    field += Mapper[2]
            field+="\n"
        print(field)
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
                    
                    field = ""
                    not_finished = self.checkWin()
                    
                    for row in range(self.field_height):
                        for col in range(self.field_width):
                            if 3 == self.field.cell[row][col]:
                                field += Mapper[3]
                            elif 0 == self.field.cell[row][col]:
                                field += Mapper[0]
                            elif 1 == self.field.cell[row][col]:
                                field += Mapper[1]
                            else:
                                field += Mapper[2]
                        field += "\n"
                    print(field)
                print("========================================")
                
                #print end1 - start1, end2 - start2
                time.sleep(1)