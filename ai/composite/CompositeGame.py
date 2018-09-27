import numpy as np

from ..Game import Game
from ..connect4.Connect4Game import Connect4Game
from ..othello.OthelloGame import OthelloGame


class CompositeGame(Game):
    def __init__(self, size):
        self.games = [Connect4Game(size, size), OthelloGame(size)]

    def getActionSize(self):
        return self.games[0].getActionSize(), self.games[1].getActionSize()

    def getBoardSize(self):
        return self.games[0].getBoardSize()
