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
                    'cpuct':  .1,
                    'arenaCompare': 2,

                    })
    # ckpt_o = [41, 43]
    ckpt_o = [16, 24]
    ckpt_c = [3, 41]
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
