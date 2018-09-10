# -*- coding: utf-8 -*-
r"""
    Behold, removing tf.Session() in the very first line will cause "interrupted by signal 11: SIGSEGV"
"""
import tensorflow as tf; tf.Session()
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow

from ai.MCTS import MCTS
from ai.othello.OthelloGame import OthelloGame as Og
from ai.othello.keras.NNet import NNetWrapper as ONNet

from ai.gobang.GobangGame import GobangGame as Gg
from ai.gobang.keras.NNet import NNetWrapper as GNNet

from ai.connect4.Connect4Game import Connect4Game as Cg
from ai.connect4.keras.NNet import NNetWrapper as CNNet
from ai.utils import *
from mainwindow import Ui_MainWindow
import numpy as np


class QMainScreen(QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.mouseReleaseEvent = self.updateText
        self.scene.mousePressEvent = self.scene_mousePressEvent
        self.ui.graphicsViewBoard.setScene(self.scene)
        self.ui.pushButtonNewGame.clicked.connect(self.startButton_click)
        self.ui.pushButtonHintToggle.clicked.connect(self.hint_toggle)
        self.ui.pushButtonAIToggle.clicked.connect(self.ai_toggle)
        self.ui.lineEditNumMCTSSims.setText("25")
        self.ui.textEditInfo.setReadOnly(True)

        self.g = Cg
        self.NNet = CNNet

        self.n = 0
        self.b = 1
        self.w = -1

        r"""nnet players"""
        self.args1 = None
        self.mcts1 = None
        self.mctsplayer = None
        self.AI = True

        r"""
            start with black
        """
        self.turn = 1
        self.hint = False

        r"""
            A game to play and a board
        """
        self.game = self.g(8, 8)
        self.board = None
        self.n1 = self.NNet(self.game)
        r"""
            Count number of pieces
        """
        self.BLACK = 0
        self.WHITE = 0
        self.startButton_click()

    def ai_toggle(self):
        self.ui.pushButtonAIToggle.setText("AI on" if self.AI else "AI off")
        self.AI = not self.AI

    def updateText(self, _):
        ended = self.game.getGameEnded(self.board, 1)
        if self.AI:
            ais = f"AI is playing {'white' if self.turn == 1 else 'black'}"
        else:
            ais = "AI is off"
        if ended == 1:
            endtext = 'Black won'
        elif ended == -1:
            endtext = 'White won'
        else:
            endtext = 'No one is won'
        self.ui.textEditInfo.setText(f'{ais}, mctsSims: {self.ui.lineEditNumMCTSSims.text()}\n'
                                     f'WHITE: {self.WHITE}, BLACK: {self.BLACK}\n{endtext}')

    def hint_toggle(self):
        self.hint = ~self.hint
        self.refresh()

    def startButton_click(self):
        weights = ['othello_8x8x60_best.pth.tar', 'othello_8x8x73_best.pth.tar']
        # weights = ['connect4_8x8x52.pth.tar', 'connect4_8x8x7.pth.tar']
        epch = self.ui.comboBoxWeightsName.currentIndex()
        self.turn = 1
        self.board = self.game.getInitBoard()
        # self.n1.load_checkpoint('ai/weights/', weights[epch])
        try:
            nsims = int(self.ui.lineEditNumMCTSSims.text())
            self.args1 = dotdict({'numMCTSSims': nsims, 'cpuct': 1.0})
        except ValueError:
            self.args1 = dotdict({'numMCTSSims': 25, 'cpuct': 1.0})
        self.mcts1 = MCTS(self.game, self.n1, self.args1)
        self.mctsplayer = lambda x: np.argmax(self.mcts1.getActionProb(x, temp=0))

        self.refresh()
        if self.AI:
            self.scene_mousePressEvent(None)
        ended = self.game.getGameEnded(self.board, 1)
        if self.AI:
            ais = f"AI is playing {'white' if self.turn == 1 else 'black'}"
        else:
            ais = "AI is off"
        if ended == 1:
            endtext = 'Black won'
        elif ended == -1:
            endtext = 'White won'
        else:
            endtext = 'No one is won'
        self.ui.textEditInfo.setText(f'{ais}, mctsSims: {self.ui.lineEditNumMCTSSims.text()}\n'
                                     f'WHITE: {self.WHITE}, BLACK: {self.BLACK}\n{endtext}')

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        self.update()

    def scene_mousePressEvent(self, event):
        if event is not None:
            x = int(event.scenePos().x() // 62)
            y = int(event.scenePos().y() // 62)
        else:
            x = 4
            y = 4
        if self.g == Og or self.g == Gg:
            action = y * 8 + x
        else:
            action = x
        valid = self.game.getValidMoves(self.board, self.turn)
        if np.sum(valid[:-1]) > 0:
            if valid[action] == 0 and event is not None:
                return
            elif event is None:
                if self.AI:
                    action = self.mctsplayer(self.game.getCanonicalForm(self.board, self.turn))
                    self.board, self.turn = self.game.getNextState(self.board, self.turn, action)

                self.refresh()
                self.update()
                return

            pr = QtCore.QRectF(QtCore.QPointF(x*62+5, y*62+5), QtCore.QSizeF(52, 52))
            if self.turn == 1:
                self.scene.addEllipse(pr, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.black))
            elif self.turn == -1:
                self.scene.addEllipse(pr, QtGui.QPen(QtCore.Qt.white), QtGui.QBrush(QtCore.Qt.white))
            self.board, self.turn = self.game.getNextState(self.board, self.turn, action)
        else:
            self.turn *= -1
        if self.AI and self.game.getGameEnded(self.board, 1) == 0:
            action = self.mctsplayer(self.game.getCanonicalForm(self.board, self.turn))
            self.board, self.turn = self.game.getNextState(self.board, self.turn, action)

        self.refresh()
        self.update()

    def refresh(self):
        self.scene.clear()
        pen = QtGui.QPen(QtCore.Qt.black)
        side = 62
        self.WHITE = 0
        self.BLACK = 0
        for y in range(8):
            for x in range(8):
                if self.g == Og or self.g == Gg:
                    action = y * 8 + x
                else:
                    action = y

                valid = self.game.getValidMoves(self.board, self.turn)
                r = QtCore.QRectF(QtCore.QPointF(x * side, y * side), QtCore.QSizeF(side, side))
                pr = QtCore.QRectF(QtCore.QPointF(x * side + 5, y * side + 5), QtCore.QSizeF(side - 10, side - 10))
                sr = QtCore.QRectF(QtCore.QPointF(x * side + 20, y * side + 20), QtCore.QSizeF(side - 40, side - 40))
                self.scene.addRect(r, pen, QtGui.QBrush(QtCore.Qt.darkGreen))
                if self.board[y][x] == self.b:
                    self.scene.addEllipse(pr, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.black))
                    self.BLACK += 1
                elif self.board[y][x] == self.w:
                    self.scene.addEllipse(pr, QtGui.QPen(QtCore.Qt.white), QtGui.QBrush(QtCore.Qt.white))
                    self.WHITE += 1
                elif valid[action] == 1 and self.hint:
                    self.scene.addEllipse(sr, QtGui.QPen(QtCore.Qt.darkBlue), QtGui.QBrush(QtCore.Qt.darkBlue))
