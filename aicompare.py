from ai.Arena import Arena
from ai.MCTS import MCTS
from ai.utils import dotdict
from ai.othello.OthelloGame import OthelloGame as Game
from ai.othello.keras.NNet import NNetWrapper as nn
import numpy as np
import time
import os
import sys
from pickle import Pickler, Unpickler
from random import shuffle


if __name__ == '__main__':
    args = dotdict({
        'numIters': 40,
        'numEps': 512,
        'tempThreshold': 15,
        'updateThreshold': 0.55,
        'maxlenOfQueue': 2000000,
        'numMCTSSims': 10,
        'arenaCompare': 20,
        'cpuct': 1,
        'max_processes': 4,
        'checkpoint': './othello8x8c4/',
        'load_model': True,
        'load_folder_file': ('./temp/', 'othelloc4.h5'),
        'numItersForTrainExamplesHistory': 20,

    })
    g = Game(8)
    c4net = nn(g)
    # c4net.load_checkpoint('ai/weights', 'othello_c4_8x8x31.pth.tar')
    c4net.load_checkpoint('ai/weights', 'othello_8x8x73_best.pth.tar')
    nnet = nn(g)
    nnet.load_checkpoint('ai/weights', 'othello_8x8x60_best.pth.tar')
    c4mcts = MCTS(g, c4net, args)
    nmcts = MCTS(g, nnet, args)
    arena = Arena(lambda x: np.argmax(c4mcts.getActionProb(x, temp=0)),
                  lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), g)
    c4wins, nwins, draws = arena.playGames(args.arenaCompare)
    print(f'\nC4 wins: {c4wins}')
    print(f'N wins: {nwins}')
    print(f'draws: {draws}')
