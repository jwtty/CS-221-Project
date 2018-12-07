# starter bot refactored from Riddles Hackman python2 starter bot
import sys

from Bot.simulator import Game
from Bot.bot import Bot

def main():
    bot = Bot()
    bot2 = Bot()
    game = Game()
    game.run(bot, bot2)

if __name__ == '__main__':
    while(1):
        main()
