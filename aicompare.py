import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

from ai.Arena import Arena
from ai.MCTS import MCTS
from ai.utils import dotdict
from ai.othello.OthelloGame import OthelloGame as Game
from ai.othello.keras.NNet import NNetWrapper as nn
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
    ckpt_o = [1, 2, 11, 15, 16, 22, 23, 24, 25, 28, 29, 31, 32, 40, 41, 43]
    ckpt_c = [1, 2, 3, 5, 7, 8, 10, 13, 20, 21, 22, 25, 26, 28, 29, 32, 39, 41, 47]
    result = []
    g = Game(8)
    c4net = nn(g)
    for o in ckpt_o:
        for c in ckpt_c:
            c4net.load_checkpoint('othello8b', f'checkpoint_{o}.pth.tar')
            # c4net.load_checkpoint('ai/weights', 'othello_8x8x73_best.pth.tar')
            nnet = nn(g)
            nnet.load_checkpoint('composite', f'1checkpoint_{c}.pth.tar')
            c4mcts = MCTS(g, c4net, args)
            nmcts = MCTS(g, nnet, args)
            arena = Arena(lambda x: np.argmax(c4mcts.getActionProb(x, temp=0)),
                          lambda x: np.argmax(nmcts.getActionProb(x, temp=0)),
                          g)
            c4wins, nwins, draws = arena.playGames(args.arenaCompare)
            result.append((c4wins, nwins, draws))
            print(f'\nNorm wins: {c4wins}')
            print(f'Composite wins: {nwins}')
            print(f'draws: {draws}')
            with open('compare_composite_o.txt', 'w') as wr:
                wr.write(str(result))
