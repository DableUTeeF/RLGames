import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

from ai.Arena import Arena
from ai.MCTS import MCTS
from ai.utils import dotdict
from ai.othello.OthelloGame import OthelloGame as Game
from ai.othello.keras.NNet import NNetWrapper as nn
import numpy as np


if __name__ == '__main__':
    args = dotdict({'numMCTSSims': 25,
                    'cpuct':  0.1,
                    'arenaCompare': 1,

                    })
    # ckpt_o = [41, 43]
    ckpt_o = [1, 2, 11, 15, 16, 21, 23, 24, 25, 28, 29, 31, 32, 40, 41, 43]
    ckpt_c = [1, 2, 3, 5, 7, 8, 10, 13, 20, 21, 22, 25, 26, 28, 29, 32, 39, 41, 47]
    result = []
    g = Game(8)
    normalnet = nn(g)
    for o in ckpt_o:
        for c in ckpt_c:
            normalnet.load_checkpoint('othello8b', f'checkpoint_{o}.pth.tar')
            # c4net.load_checkpoint('ai/weights', 'othello_8x8x73_best.pth.tar')
            compositenet = nn(g)
            compositenet.load_checkpoint('composite', f'1checkpoint_{c}.pth.tar')
            c4mcts = MCTS(g, normalnet, args)
            nmcts = MCTS(g, compositenet, args)
            arena = Arena(lambda x: np.argmax(c4mcts.getActionProb(x, temp=0)),
                          lambda x: np.argmax(nmcts.getActionProb(x, temp=0)),
                          g)
            normalwins, compositewins, draws = arena.playGames(args.arenaCompare)
            result.append((normalwins, compositewins, draws))
            print(f'\nNorm wins: {normalwins}')
            print(f'Composite wins: {compositewins}')
            print(f'draws: {draws}')
            with open('compare_composite_o3.txt', 'w') as wr:
                wr.write(str(result))
