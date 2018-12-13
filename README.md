# AI Agent for Light Rider -- CS221 Final Project at Stanford

*Authors: Yipeng He, Wantong Jiang, Di Bai*

This is our final project for CS221 AI Fall 2018 at Stanford. 

In this project, we implemented an AI agent for game Light Rider.
The game is originally provided by [Riddles.io](https://playground.riddles.io/competitions/light-riders). 

The project contains:
- A simulator written by us to run 'Light Rider' game.
- Minimax agents with different settings and a linear Q-Learning agent trained against minimax agents.

## Quick Start

```
cd Bot
python main.py
```
Enter the `Bot` directory, and run `main.py`. It will automatically start training a Q-Learning agent against a minimax agent.

## Parameters
```
--mode game|rl # change mode fron Q-Learning to minimax competition
--grid 6 # change the grid size to 6
--rl_trial 10000 # change Q-Learning trial number to 10000
--test_rl # whether to test a trained Q-Learning agent
--rl_weights weights.txt # read from weights.txt to get learned parameters for Q-Learning agent
--rl_save file.txt # save learned paraments for Q-Learning agent
```
For more details, run
```
python main.py -h
```

To change the settings of two minimax agents in the game mode, please look into `Bot/simulator.py`.

To change the setting of the minimax agent against Q-Learning agent, please look into `Bot/rl.py`.

## File Struture

- `board.py` implements board information, update, and print
- `bot.py` implements bot interface
- `game.py` implements interface with Riddles.io
- `minimax.py` implements minimax agent, minimax with alphabeta agent and different evaluation functions
- `player.py` implements player class, containing player's position
- `rl.py` implements Q-Learning agent and training against minimax agent
- `simulator.py` implements two player game simulator
- `state.py` implements game state
- `util.py` implements parameter parsing

## License
[MIT License](LICENSE)

