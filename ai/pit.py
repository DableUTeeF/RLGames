from ai import Arena
from ai.MCTS import MCTS
# from ai.othello.OthelloGame import OthelloGame, display
# from ai.othello.OthelloPlayers import *
# from ai.othello.keras.NNet import NNetWrapper as NNet
from ai.connect4.Connect4Game import Connect4Game, display
from ai.connect4.Connect4Players import *
from ai.connect4.keras.NNet import NNetWrapper as NNet

import numpy as np
from ai.utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = Connect4Game(8)

# all players
rp = RandomPlayer(g).play
# gp = GreedyConnect4Player(g).play
hp = HumanConnect4Player(g).play

# nnet players
n1 = NNet(g)
# n1.load_checkpoint('weights/', '8x8x60_best.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

arena = Arena.Arena(n1p, hp, g, display=display)
print(arena.playGames(2, verbose=True))
