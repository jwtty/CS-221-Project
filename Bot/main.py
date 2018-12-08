# starter bot refactored from Riddles Hackman python2 starter bot
import sys

from Bot.simulator import Game
from Bot.bot import Bot
from Bot.rl import RLAlgorithm
from Bot.util import parse_args

def main(grid_size):
    bot = Bot()
    bot2 = Bot()
    game = Game()
    game.field_width = game.field_height = grid_size
    game.run(bot, bot2)

def mainrl(trials, save, read, test, grid):
    rl = RLAlgorithm(0.99)
    rl.train(verbose=True, num_trials=trials, save_file=save, read_file=read, test = test, grid_size=grid)
    
if __name__ == '__main__':
    args = parse_args()
    mode = args.mode
    grid_size = args.grid
    if mode == "game":
        main(grid_size)
    elif mode == "rl":
        read_file = args.rl_weights
        save_file = args.rl_save
        test = args.test_rl
        trials = args.rl_trial
        mainrl(trials, save_file, read_file, test, grid_size)
