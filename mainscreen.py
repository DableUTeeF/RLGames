# -*- coding: utf-8 -*-
r"""
    Behold, removing tf.Session() in the very first line will cause "interrupted by signal 11: SIGSEGV".
    You need to initiate a Session to reserve GPU's memory for some reason.
    At least, in my tensorflow 1.4.0.
"""
import tensorflow as tf; tf.Session()
from PyQt5 import QtCore, QtWidgets, QtGui, QtTest, QtSvg
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QFont, QImage, QPalette, QBrush
from PIL import ImageQt, Image
from ai.MCTS import MCTS
from ai.othello.OthelloGame import OthelloGame as Og
from ai.othello.keras.NNet import NNetWrapper as ONNet

from ai.gobang.GobangGame import GobangGame as Gg
from ai.gobang.keras.NNet import NNetWrapper as GNNet

from ai.connect4.Connect4Game import Connect4Game as Cg
from ai.connect4.keras.NNet import NNetWrapper as CNNet
from ai.utils import *
from mainwindow import Ui_MainWindow
from newgame import Ui_NewGame
import time
import numpy as np
import os


class QMainScreen(QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QtWidgets.QGraphicsScene()
        # self.scene.mouseReleaseEvent = self.updateText
        self.scene.mousePressEvent = self.scene_mousePressEvent
        self.ui.graphicsViewBoard.setScene(self.scene)
        self.ui.actionNewGame.triggered.connect(self.startButton_click)
        self.ui.actionHint.triggered.connect(self.hint_toggle)
        self.ui.actionAI.triggered.connect(self.ai_toggle)
        self.ui.blackLcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.ui.whiteLcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        # self.ui.statusBar.hide()

        self.bg = ImageQt.ImageQt(Image.open('img/board2.png'))
        self.tatami = QImage('img/tatami.png').mirrored()
        palette = QPalette()
        # noinspection PyTypeChecker
        palette.setBrush(10, QBrush(self.tatami))
        self.setPalette(palette)
        self.newgame = QtWidgets.QMdiSubWindow()
        self.newgamewindow = Ui_NewGame()
        self.newgamewindow.setupUi(self.newgame)
        self.newgame.setFixedSize(self.newgame.size())
        self.newgamewindow.whichGameBox.currentIndexChanged.connect(self.whichGameChanged)
        self.newgamewindow.boardSizeBox_h.currentIndexChanged.connect(self.newwindow_boardsize_h)
        self.newgamewindow.boardSizeBox_w.currentIndexChanged.connect(self.newwindow_boardsize_w)
        self.newgamewindow.CancleButton.clicked.connect(self.cancleclick)
        self.newgamewindow.OKButton.clicked.connect(self.startgame)
        self.initiate_newgame()

        self.g = Og
        self.NNet = ONNet

        self.recentMove = [0, 0, 0]
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
        self.game = self.g(8)
        self.board = None
        self.n1 = self.NNet(self.game)
        r"""
            Count number of pieces
        """
        self.BLACK = 0
        self.WHITE = 0
        self.startgame(None)

    # -------------------------------- New Game -------------------------------- #
    def initiate_newgame(self):
        self.newgamewindow.whichGameBox.clear()
        self.newgamewindow.whichGameBox.addItem('Othello')
        self.newgamewindow.whichGameBox.addItem('Connect4')
        self.newgamewindow.boardSizeBox_h.addItem('6')
        self.newgamewindow.boardSizeBox_w.addItem('6')
        self.newgamewindow.boardSizeBox_h.addItem('8')
        self.newgamewindow.boardSizeBox_w.addItem('8')
        self.newgamewindow.boardSizeBox_h.addItem('10')
        self.newgamewindow.boardSizeBox_w.addItem('10')

    def newwindow_boardsize_h(self, _):
        if self.newgamewindow.whichGameBox.currentIndex() == 0:
            self.newgamewindow.boardSizeBox_w.setCurrentIndex(self.newgamewindow.boardSizeBox_h.currentIndex())

    def newwindow_boardsize_w(self, _):
        if self.newgamewindow.whichGameBox.currentIndex() == 0:
            self.newgamewindow.boardSizeBox_h.setCurrentIndex(self.newgamewindow.boardSizeBox_w.currentIndex())

    def whichGameChanged(self, gameidx):
        # ----- Board size ----- #
        self.newgamewindow.boardSizeBox_h.clear()
        self.newgamewindow.boardSizeBox_w.clear()
        self.newgamewindow.boardSizeBox_h.addItem('6')
        self.newgamewindow.boardSizeBox_w.addItem('6')
        if gameidx == 1:
            self.newgamewindow.boardSizeBox_h.addItem('7')
            self.newgamewindow.boardSizeBox_w.addItem('7')
        self.newgamewindow.boardSizeBox_h.addItem('8')
        self.newgamewindow.boardSizeBox_w.addItem('8')
        self.newgamewindow.boardSizeBox_h.addItem('10')
        self.newgamewindow.boardSizeBox_w.addItem('10')
        self.newgamewindow.boardSizeBox_h.setCurrentIndex(1)
        self.newgamewindow.boardSizeBox_w.setCurrentIndex(1)

        # ------ Weights ------ #
        self.newgamewindow.weightBox.clear()
        for file in os.listdir('ai/weights'):
            if self.newgamewindow.whichGameBox.currentIndex() == 0:
                if file.startswith('othello'):
                    self.newgamewindow.weightBox.addItem(file)
            elif self.newgamewindow.whichGameBox.currentIndex() == 1:
                if file.startswith('connect4'):
                    self.newgamewindow.weightBox.addItem(file)

    def cancleclick(self, _):
        self.newgame.hide()
    # ------------------------------ Main Window ------------------------------- #

    def ai_toggle(self, _):
        self.AI = not self.AI
        self.refresh()

    def updateText(self):
        if self.game.getGameEnded(self.board, self.turn):
            return
        bfont = QFont()
        wfont = QFont()
        self.ui.blackLcdNumber.display(str(self.BLACK))
        self.ui.whiteLcdNumber.display(str(self.WHITE))
        aipalette = self.ui.whiteLcdNumber.palette()
        humanpalette = self.ui.blackLcdNumber.palette()
        # Text
        aipalette.setColor(aipalette.WindowText, QtGui.QColor(255, 0, 0))
        humanpalette.setColor(humanpalette.WindowText, QtGui.QColor(0, 0, 255))
        # # "light" border
        aipalette.setColor(aipalette.Light, QtGui.QColor(255, 85, 85))
        humanpalette.setColor(humanpalette.Light, QtGui.QColor(85, 85, 255))
        # # "dark" border
        # aipalette.setColor(aipalette.Dark, QtGui.QColor(150, 60, 60))
        # humanpalette.setColor(humanpalette.Dark, QtGui.QColor(60, 60, 150))
        self.ui.whiteLcdNumber.setPalette(humanpalette)
        self.ui.blackLcdNumber.setPalette(aipalette)

        if self.turn == self.b:
            bfont.setBold(True)
            bfont.setUnderline(True)
            self.ui.blackLabel.setFont(bfont)
            self.ui.whiteLabel.setFont(wfont)

            if self.ui.actionAI.isChecked():
                self.ui.rightPlayerLabel.setText('AI')
                self.ui.leftPlayerLabel.setText('Human')
            else:
                self.ui.rightPlayerLabel.setText('Human')
                self.ui.leftPlayerLabel.setText('Human')
        else:
            wfont.setBold(True)
            wfont.setUnderline(True)
            self.ui.blackLabel.setFont(bfont)
            self.ui.whiteLabel.setFont(wfont)

            if self.ui.actionAI.isChecked():
                self.ui.rightPlayerLabel.setText('Human')
                self.ui.leftPlayerLabel.setText('AI')
            else:
                self.ui.rightPlayerLabel.setText('Human')
                self.ui.leftPlayerLabel.setText('Human')

    def hint_toggle(self, _):
        self.hint = ~self.hint
        self.refresh()

    def startButton_click(self, _):
        self.newgame.show()

    def startgame(self, _):
        if self.newgamewindow.whichGameBox.currentIndex() == 0:
            # self.resize(600, 600)
            self.setFixedSize(self.size())
            self.ui.frame.show()
        else:
            # self.resize(600, 600)
            self.setFixedSize(self.size())
            self.ui.frame.hide()

        if self.newgamewindow.whichGameBox.currentIndex() == 0 and self.g != Og:
            self.g = Og
            self.NNet = ONNet
            self.game = self.g(int(self.newgamewindow.boardSizeBox_h.currentText()))
            self.n1 = self.NNet(self.game)
        elif self.newgamewindow.whichGameBox.currentIndex() == 1 and self.g != Cg:
            self.g = Cg
            self.NNet = CNNet
            self.game = self.g(int(self.newgamewindow.boardSizeBox_w.currentText()),
                               int(self.newgamewindow.boardSizeBox_h.currentText()))
            self.n1 = self.NNet(self.game)
        weights = self.newgamewindow.weightBox.currentText()
        self.turn = 1
        self.board = self.game.getInitBoard()
        self.n1.load_checkpoint('ai/weights/', weights)
        try:
            nsims = int(self.newgamewindow.mctsSimsBox.value())
            self.args1 = dotdict({'numMCTSSims': nsims, 'cpuct': 1.0})
        except ValueError:
            self.args1 = dotdict({'numMCTSSims': 25, 'cpuct': 1.0})
        self.mcts1 = MCTS(self.game, self.n1, self.args1)
        self.mctsplayer = lambda x: np.argmax(self.mcts1.getActionProb(x, temp=0))

        self.refresh()
        if self.newgamewindow.aiTurnBox.isChecked():
            self.aimove()
        self.newgame.hide()
        self.updateText()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        self.update()

    # noinspection PyArgumentList
    def scene_mousePressEvent(self, event):
        x = int(event.scenePos().x() // 62)
        y = int(event.scenePos().y() // 62)
        if self.g == Og or self.g == Gg:
            action = y * 8 + x
        else:
            action = x
        valid = self.game.getValidMoves(self.board, self.turn)
        if valid[action] == 0:
            return

        self.board, self.turn = self.game.getNextState(self.board, self.turn, action)
        self.recentMove = [x, y, self.turn]
        self.refresh()
        if self.ui.actionAI.isChecked() and self.game.getGameEnded(self.board, 1) == 0:
            QtTest.QTest.qWait(200)
            while True:
                self.aimove()
                valid = self.game.getValidMoves(self.board, self.turn)
                if np.sum(valid[:-1]) > 0:
                    break
                else:
                    self.turn *= -1
                    QtTest.QTest.qWait(600)
        self.updateText()

    def aimove(self):
        action = self.mctsplayer(self.game.getCanonicalForm(self.board, self.turn))
        self.board, self.turn = self.game.getNextState(self.board, self.turn, action)
        self.recentMove = [action % 8, action // 8, self.turn]
        self.refresh()

    def refresh(self):
        self.scene.clear()
        pen = QtGui.QPen(QtCore.Qt.black)
        pixMap = QtGui.QPixmap.fromImage(self.bg)
        self.scene.addPixmap(pixMap)
        # self.ui.graphicsViewBoard.bac
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
                sr = QtCore.QRectF(QtCore.QPointF(x * side + 25, y * side + 25), QtCore.QSizeF(side - 48, side - 48))
                self.scene.addRect(r, pen)
                if self.board[y][x] == self.b:
                    stone = QtSvg.QGraphicsSvgItem('img/stone_1.svg')
                    stone.setPos(x * side + 5, y * side + 5)
                    stone.setScale(1.25)
                    self.scene.addItem(stone)
                    self.BLACK += 1
                    if [x, y, self.turn] == self.recentMove:
                        self.scene.addEllipse(sr, QtGui.QPen(QtCore.Qt.white), QtGui.QBrush(QtCore.Qt.white))
                elif self.board[y][x] == self.w:
                    stone = QtSvg.QGraphicsSvgItem('img/stone_-1.svg')
                    stone.setPos(x * side + 5, y * side + 5)
                    stone.setScale(1.25)
                    self.scene.addItem(stone)
                    self.WHITE += 1
                    if [x, y, self.turn] == self.recentMove:
                        self.scene.addEllipse(sr, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.black))
                elif valid[action] == 1 and self.hint:
                    if self.newgamewindow.aiTurnBox.isChecked() or self.AI:
                        stone = QtSvg.QGraphicsSvgItem('img/stone_h0.svg')
                    elif self.turn == self.w:
                        stone = QtSvg.QGraphicsSvgItem('img/stone_h-1.svg')
                    else:
                        stone = QtSvg.QGraphicsSvgItem('img/stone_h1.svg')
                    stone.setPos(x * side + 20, y * side + 20)
                    stone.setScale(.5)
                    self.scene.addItem(stone)
        self.update()
