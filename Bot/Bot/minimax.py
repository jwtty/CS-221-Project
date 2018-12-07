import sys
import traceback
import random
import time
import copy
from collections import deque
DIRS = [
    ((-1, 0), "up"),
    ((1, 0), "down"),
    ((0, 1), "right"),
    ((0, -1), "left")
]
from . import state

'''
Evaluation Functions with different strategies
'''

def allDirEvalFunc(curState, agent):
    my_player = curState.players[agent]
    total_score = 0
    moves = DIRS
    id = agent
    #total_score = []
    for move in moves:
        row = my_player.row
        col = my_player.col
        dir = move[0]
        iter = 15
        count = 0
        while (curState.board.in_bounds(row, col) and count < iter):
            row += dir[0]
            col += dir[1]
            if not curState.board.is_legal(row, col, id):
                break
            count += 1
        exploreDir =[ (-dir[1], -dir[0]), (dir[1], dir[0])]
        counts = [None, None]
        minSum = -1
        mid = count // 2
        for i in range(1, mid):
            row = my_player.row + dir[0]*i
            col = my_player.col + dir[1]*i
            sumCounter = 0
            cnt = []
            for direction in exploreDir:
                counter = 0
                row += direction[0]
                col += direction[1]
                while (curState.board.in_bounds(row, col) and counter < iter):
                    row += dir[0]
                    col += dir[1]
                    if not curState.board.is_legal(row, col, id):
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
        if count and counts[0] and counts[1]:
            total_score +=  weight1*count + weight2*counts[0] + weight3*counts[1]
    return total_score

def maxDirEvalFunc(curState, agent):
    my_player = curState.players[agent]
    moves = DIRS
    id = agent
    total_score = []
    for move in moves:
        row = my_player.row
        col = my_player.col
        dir = move[0]
        iter = 15
        count = 0
        while (curState.board.in_bounds(row, col) and count < iter):
            row += dir[0]
            col += dir[1]
            if not curState.board.is_legal(row, col, id):
                break
            count += 1
        exploreDir =[ (-dir[1], -dir[0]), (dir[1], dir[0])]
        counts = [None, None]
        minSum = -1
        mid = count // 2
        for i in range(1, mid):
            row = my_player.row + dir[0]*i
            col = my_player.col + dir[1]*i
            sumCounter = 0
            cnt = []
            for direction in exploreDir:
                counter = 0
                row += direction[0]
                col += direction[1]
                while (curState.board.in_bounds(row, col) and counter < iter):
                    row += dir[0]
                    col += dir[1]
                    if not curState.board.is_legal(row, col, id):
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
        if count and counts[0] and counts[1]:
            total_score.append(weight1*count + weight2*counts[0] + weight3*counts[1])
    if len(total_score) == 0:
        return 0
    return max(total_score)

def attackEvalFunc(curState, agent):
    my_player = curState.players[agent]
    total_score = 0
    moves = DIRS
    id = agent
    #total_score = []
    for move in moves:
        row = my_player.row
        col = my_player.col
        dir = move[0]
        iter = 15
        count = 0
        while (curState.board.in_bounds(row, col) and count < iter):
            row += dir[0]
            col += dir[1]
            if not curState.board.is_legal(row, col, id):
                break
            count += 1
        exploreDir =[ (-dir[1], -dir[0]), (dir[1], dir[0])]
        counts = [None, None]
        minSum = -1
        mid = count // 2
        for i in range(1, mid):
            row = my_player.row + dir[0]*i
            col = my_player.col + dir[1]*i
            sumCounter = 0
            cnt = []
            for direction in exploreDir:
                counter = 0
                row += direction[0]
                col += direction[1]
                while (curState.board.in_bounds(row, col) and counter < iter):
                    row += dir[0]
                    col += dir[1]
                    if not curState.board.is_legal(row, col, id):
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
        if count and counts[0] and counts[1]:
            total_score +=  weight1*count + weight2*counts[0] + weight3*counts[1]
    opponent = curState.players[agent ^ 1]
    dist = abs(my_player.row - opponent.row) + abs(my_player.col - opponent.col)
    return total_score + 800 * dist**-1

def blockEvalFunc(curState, agent):
    my_player = curState.players[agent]
    total_score = 0
    moves = DIRS
    id = agent
    #total_score = []
    for move in moves:
        row = my_player.row
        col = my_player.col
        dir = move[0]
        iter = 15
        count = 0
        while (curState.board.in_bounds(row, col) and count < iter):
            row += dir[0]
            col += dir[1]
            if not curState.board.is_legal(row, col, id):
                break
            count += 1
        exploreDir =[ (-dir[1], -dir[0]), (dir[1], dir[0])]
        counts = [None, None]
        minSum = -1
        mid = count // 2
        for i in range(1, mid):
            row = my_player.row + dir[0]*i
            col = my_player.col + dir[1]*i
            sumCounter = 0
            cnt = []
            for direction in exploreDir:
                counter = 0
                row += direction[0]
                col += direction[1]
                while (curState.board.in_bounds(row, col) and counter < iter):
                    row += dir[0]
                    col += dir[1]
                    if not curState.board.is_legal(row, col, id):
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
        if count and counts[0] and counts[1]:
            total_score +=  weight1*count + weight2*counts[0] + weight3*counts[1]

    opponent = curState.players[agent ^ 1]
    
    def findBlock(agent):
        x = curState.players[agent].row
        y = curState.players[agent].col
        search_queue = deque()
        search_queue.append(x * 16 + y)
        visited = set()
        while search_queue:
            num = search_queue.popleft() 
            dx = int(num/16)
            dy = int(num%16)
            if curState.board.is_legal(dx + 1, dy, agent) and (dx + 1, dy) not in visited:
                search_queue.append((dx + 1) * 16 + dy)
                visited.add((dx + 1, dy))
            if curState.board.is_legal(dx - 1, dy, agent) and (dx - 1, dy) not in visited:
                search_queue.append((dx - 1) * 16 + dy)
                visited.add( (dx - 1, dy))
            if curState.board.is_legal(dx, dy + 1, agent) and (dx, dy + 1) not in visited:
                search_queue.append(dx* 16 + dy + 1)
                visited.add( (dx, dy + 1))
            if curState.board.is_legal(dx, dy - 1, agent) and (dx, dy - 1) not in visited:
                search_queue.append(dx* 16 + dy - 1)
                visited.add( (dx, dy - 1))
            if len(search_queue) == 1:
                break
        return num/16, num%16
    
    tx, ty = findBlock(agent ^ 1)
    dist = abs(my_player.row - tx) + abs(my_player.col - ty)
    return total_score + 800 * dist**-1
    
def attackAndBlockEvalFunc(curState, agent):
    my_player = curState.players[agent]
    total_score = 0
    moves = DIRS
    id = agent
    #total_score = []
    for move in moves:
        row = my_player.row
        col = my_player.col
        dir = move[0]
        iter = 15
        count = 0
        while (curState.board.in_bounds(row, col) and count < iter):
            row += dir[0]
            col += dir[1]
            if not curState.board.is_legal(row, col, id):
                break
            count += 1
        exploreDir =[ (-dir[1], -dir[0]), (dir[1], dir[0])]
        counts = [None, None]
        minSum = -1
        mid = count // 2
        for i in range(1, mid):
            row = my_player.row + dir[0]*i
            col = my_player.col + dir[1]*i
            sumCounter = 0
            cnt = []
            for direction in exploreDir:
                counter = 0
                row += direction[0]
                col += direction[1]
                while (curState.board.in_bounds(row, col) and counter < iter):
                    row += dir[0]
                    col += dir[1]
                    if not curState.board.is_legal(row, col, id):
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
        if count and counts[0] and counts[1]:
            total_score +=  weight1*count + weight2*counts[0] + weight3*counts[1]
    opponent = curState.players[agent ^ 1]
    
    def findBlock(agent):
        x = curState.players[agent].row
        y = curState.players[agent].col
        search_queue = deque()
        search_queue.append(x * 16 + y)
        visited = set()
        while search_queue:
            num = search_queue.popleft() 
            dx = int(num/16)
            dy = int(num%16)
            if curState.board.is_legal(dx + 1, dy, agent) and (dx + 1, dy) not in visited:
                search_queue.append((dx + 1) * 16 + dy)
                visited.add((dx + 1, dy))
            if curState.board.is_legal(dx - 1, dy, agent) and (dx - 1, dy) not in visited:
                search_queue.append((dx - 1) * 16 + dy)
                visited.add( (dx - 1, dy))
            if curState.board.is_legal(dx, dy + 1, agent) and (dx, dy + 1) not in visited:
                search_queue.append(dx* 16 + dy + 1)
                visited.add( (dx, dy + 1))
            if curState.board.is_legal(dx, dy - 1, agent) and (dx, dy - 1) not in visited:
                search_queue.append(dx* 16 + dy - 1)
                visited.add( (dx, dy - 1))
            if len(search_queue) == 1:
                break
        return num/16, num%16
    
    tx, ty = findBlock(agent ^ 1)
    dist = abs(my_player.row - tx) + abs(my_player.col - ty)
    opponent = curState.players[agent ^ 1]
    dist2 = abs(my_player.row - opponent.row) + abs(my_player.col - opponent.col)
    return total_score + 500 * dist**-1 + 800 * dist2**-1
       
class SearchAgent():
    '''
    Parent class for minimaxAgent and AlphabetaAgent
    '''
    def __init__(self, evalFunc = attackAndBlockEvalFunc, depth = 2):
        self.evaluationFunction = evalFunc
        self.depth = depth
    
    def getAction(self, curAgent, gameState):
        # Default: return a random action
        legalActions = gameState.getLegalActions(curAgent)
        return random.choice(legalActions)

class MinimaxAgent(SearchAgent):
    
    def getAction(self, curAgent, gameState):
        depth = self.depth
        def actionAndScore(curState, depth, agent):
            legalActions = curState.getLegalActions(agent)
            if depth == 0:
                return [None, self.evaluationFunction(curState, agent)]
            elif curState.isEnd(agent):
                return [None, curState.getMyReward(curAgent)]
            else:
                nextAgent = curState.getNextPlayer(agent)
                if agent == curAgent^1:
                    depth = depth - 1 
                nextScores = [actionAndScore(curState.generateSuccessor(agent,action), depth, nextAgent)[1] for action in legalActions]
                if agent == curAgent:
                    max_index, max_value = max(enumerate(nextScores), key= lambda x: x[1])
                    return [legalActions[max_index], max_value]
                else:
                    min_index, min_value = min(enumerate(nextScores), key= lambda x: x[1])
                    return [legalActions[min_index], min_value]

        action, score = actionAndScore(gameState, depth, curAgent)
        return action

class AlphaBetaAgent(SearchAgent):

    def getAction(self, curAgent, gameState):
        depth = self.depth
        def actionAndScore(curState, depth, agent, alpha, beta):
            legalActions = curState.getLegalActions(agent)
            if depth == 0:
                return [None, self.evaluationFunction(curState, agent)]
            elif curState.isEnd(agent):
                return [None, curState.getMyReward(curAgent)]
            else:
                nextAgent = curState.getNextPlayer(agent)
                if agent == curAgent^1:
                    depth = depth - 1 
                if agent == curAgent:
                    maxv = alpha
                    maxaction = None
                    for action in legalActions:
                        nxtpair = actionAndScore(curState.generateSuccessor(agent, action), depth, nextAgent, maxv, beta)
                        if nxtpair[1] > maxv:
                            maxv = nxtpair[1]
                            maxaction = action
                        if maxv >= beta:
                            break
                    return [maxaction, maxv]
                else:
                    minv = beta
                    minaction = None
                    for action in legalActions:
                        nxtpair = actionAndScore(curState.generateSuccessor(agent, action), depth, nextAgent, alpha, minv)
                        if nxtpair[1] < minv:
                            minv = nxtpair[1]
                            minaction = action
                        if minv <= alpha:
                            break
                    return [minaction, minv]

        action, score = actionAndScore(gameState, depth, curAgent, float("-inf"), float("+inf"))
        return action