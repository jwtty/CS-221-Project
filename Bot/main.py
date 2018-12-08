# starter bot refactored from Riddles Hackman python2 starter bot
import sys

from Bot.simulator import Game
from Bot.bot import Bot
from Bot.rl import RLAlgorithm

def main():
    bot = Bot()
    bot2 = Bot()
    game = Game()
    game.run(bot, bot2)

def mainrl():
    rl = RLAlgorithm(0.99)
    rl.train(verbose=True)
if __name__ == '__main__':
    #main()
    mainrl()
