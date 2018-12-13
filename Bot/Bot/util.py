import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_rl", type=str, default=False, help="whether to test a rl agent (sets explore prob to 0)")
    parser.add_argument("--rl_weights", type=str, default=None, help="the weight file for RL agent, used for restore weight parameters")
    parser.add_argument("--rl_save", type=str, default=None, help="file name to save the weigts for RL agent")
    parser.add_argument("--rl_trial", type=int, default=20000, help="num_trials the rl is going to use")
    parser.add_argument("--mode", type=str, default="rl", help="game|rl whether to enter game play or rl training")
    parser.add_argument("--grid", type=int, default=4, help="size of grid, should match with grid used for rl training if hoping to use")
    args = parser.parse_args()
    return args