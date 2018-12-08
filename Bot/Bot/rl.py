
import random, math, pickle, time
import numpy as np
from . import state
from . import simulator
from . import bot
from . import minimax
from copy import deepcopy
from collections import defaultdict, Counter

class RLAlgorithm(object):

    def __init__(self, discount, explorationProb = 0.2):
        self.discount = discount
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def __str__(self):
        return "RLAlgorithm"


    def featureExtractor(self, state, action):
        featureKey = (state.board.tostring(), action)
        featureValue = 1
        return [(featureKey, featureValue)]

    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    def getAction(self, state, agent):
        self.numIters += 1
        legalactions = state.getLegalActions(agent)
        if len(legalactions) == 0:
            return None

        if random.random() < self.explorationProb:
            return random.choice(legalactions)
        else:
            return max((self.getQ(state, action), action) for action in legalactions)[1]

    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    def incorporateFeedback(self, state, action, reward, newState, agent):
        if newState is None:
            return
        Qopt = self.getQ(state, action)
        Vopt = 0
        if not newState is None:
            for newAction in newState.getLegalActions(agent):
                Vopt = max(Vopt, self.getQ(newState, newAction))

        for f, v in self.featureExtractor(state, action):
            self.weights[f] = self.weights[f] - self.getStepSize() * (Qopt - (reward + self.discount * Vopt)) * v

    def train(self, num_trials=20000, verbose=False, save_file = None, read_file = None, test = False, grid_size = 4):
        print "RL training"
        totalRewards = []  # The rewards we get on each trial
        win = 0
        totalWin = 0
        winRecord = []
        draw = 0
        totalDraw = 0
        drawRecord = []

        if read_file:
            # Support read from file and get learned weights
            self.read(read_file)
        if test:
            # When testing, do not explore, just exploit
            self.explorationProb = 0

        for trial in xrange(num_trials):
            if trial == num_trials - 399:
                self.explorationProb = 0.0
            game = simulator.Game()
            game.field_height = game.field_width = grid_size
            game.initialize()
            bot1 = bot.Bot()
            bot1.setup(game)
            totalDiscount = 1
            totalReward = 0
            rewards = []

            while not game.current_state.isEnd(0):
                action1 = bot1.do_turn(mmAgent = minimax.MinimaxAgent(evalFunc = minimax.allDirEvalFunc, depth = 3))
                actionRL = self.getAction(game.current_state, 1) # hard code...
                game.previous_state = deepcopy(game.current_state)
                game.update_field(action1, actionRL)
                game.update_players(action1, actionRL)

                reward = 0
                e = game.current_state.isEnd(1) #the RL agent is set to player 1 by default
                if e == 1:
                    reward = 100
                elif e == -1 or e == 2:
                    reward = -100
                rewards.append(reward)

                totalReward += totalDiscount * reward
                totalDiscount *= self.discount
                self.incorporateFeedback(game.previous_state, actionRL, reward, game.current_state, 1)

            winres = game.checkWin()
            if winres == 2:
                win += 1
                totalWin += 1
            elif winres == 3:
                draw += 1
                totalDraw += 1

            if verbose:
                print "Trial %d (totalReward = %s)" % (trial, totalReward)
            totalRewards.append(totalReward)

            if trial % 100 == 99:
                print("win_rate in the last 100 trials:", win / 100.0)
                print("draw_rate in the last 100 trials:", draw / 100.0)
                winRecord.append(win)
                drawRecord.append(draw)
                win = 0
                draw = 0

        if save_file:
            # save the learned weights into `save_file`
            file = open(save_file, "w")
            for key in self.weights:
                keys = [str(key[0]), str(key[1][0]), str(key[1][1])]
                file.write(":".join(keys) + ":" + str(self.weights[key]) + "\n")
            file.close()

        print "Average reward:", sum(totalRewards)/num_trials
        print "Average wins:", totalWin * 1.0 /num_trials
        print "Win Record:", winRecord
        print "Average draws:", totalDraw * 1.0 / num_trials
        print "Draw Record:", drawRecord
        return totalRewards

    def read(self, weight_file = "qlearning.txt"):
        file = open(weight_file, "r")
        lines = file.readlines()
        for line in lines:
            keyWeight = line.split(":")
            state = keyWeight[0]
            dir = (int(keyWeight[1][1:-1].split(",")[0]),int(keyWeight[1][1:-1].split(",")[-1]))
            dirString = keyWeight[2]
            key = ((state,(dir, dirString)))
            weight = float(keyWeight[-1][:-1])
            self.weights[key] = weight
        file.close()
