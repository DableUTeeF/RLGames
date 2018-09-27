import os
import numpy as np
import sys
import tensorflow as tf

sys.path.append('..')
from ...utils import *

from .CompositeNNet import CompositeNNet as Cnnet

args = dotdict({
    'lr': 0.0001,
    'dropout': 0.3,
    'epochs': 1,
    'batch_size': 4096,
    'cuda': True,
    'num_channels': 512,
    'train': False,
})


class NNetWrapper:
    def __init__(self, game):
        self.graph = tf.get_default_graph()
        self.nnet = Cnnet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

    def train(self, examples):
        """
        examples: list of list of examples, each example is of form (board, pi, v)
        """
        for i in range(2):
            input_boards, target_pis, target_vs = list(zip(*examples[i]))
            input_boards = np.asarray(input_boards)
            target_pis = np.asarray(target_pis)
            target_vs = np.asarray(target_vs)
            self.nnet.model[i].fit(x=input_boards, y=[target_pis, target_vs], batch_size=args.batch_size, epochs=args.epochs)

    def predict(self, board, gindex):
        """
        board: np array with board
        """
        # timing
        # start = time.time()

        # preparing input
        board = board[np.newaxis, :, :]
        with self.graph.as_default():
            # run
            self.nnet.model[gindex]._make_predict_function()
            pi, v = self.nnet.model[gindex].predict(board)

        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        for i in range(2):
            filepath = os.path.join(folder, str(i)+filename)
            if not os.path.exists(folder):
                print("Checkpoint Directory does not exist! Making directory {}".format(folder))
                os.mkdir(folder)
            else:
                print("Checkpoint Directory exists! ")
            self.nnet.model[i].save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        for i in range(2):
            filepath = os.path.join(folder, str(i)+filename)
            if not os.path.exists(filepath):
                raise ("No model in path {}".format(filepath))
            self.nnet.model[i].load_weights(filepath)
