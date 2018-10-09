from ai.Arena import Arena
from ai.MCTS import MCTS
from ai.utils import dotdict
from ai.connect4.Connect4Game import Connect4Game as Game
from ai.connect4.keras.NNet import NNetWrapper as nn
import numpy as np


if __name__ == '__main__':
    args = dotdict({
        'numIters': 40,
        'numEps': 512,
        'tempThreshold': 15,
        'updateThreshold': 0.55,
        'maxlenOfQueue': 2000000,
        'numMCTSSims': 3,
        'arenaCompare': 100,
        'cpuct': 1,
        'max_processes': 4,
        'checkpoint': './othello8x8c4/',
        'load_model': True,
        'load_folder_file': ('./temp/', 'othelloc4.h5'),
        'numItersForTrainExamplesHistory': 20,

    })
    g = Game(8, 8)
    c4net = nn(g)
    c4net.load_checkpoint('ai/weights', 'connect4_8x8x5.tar')
    # c4net.load_checkpoint('ai/weights', 'othello_8x8x73_best.pth.tar')
    nnet = nn(g)
    nnet.load_checkpoint('ai/weights', 'connect4_o_8x8x11.pth.tar')
    c4mcts = MCTS(g, c4net, args)
    nmcts = MCTS(g, nnet, args)
    arena = Arena(lambda x: np.argmax(c4mcts.getActionProb(x, temp=0)),
                  lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), g)
    c4wins, nwins, draws = arena.playGames(args.arenaCompare)
    print(f'\nC4b wins: {c4wins}')
    print(f'C4 wins: {nwins}')
    print(f'draws: {draws}')
