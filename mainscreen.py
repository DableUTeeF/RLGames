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
import pyscreenshot as screenshot
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
import platform

# todo: 1.train with c4 weights(in progress)
# todo: 2.train with head fixed weights(see testdiffheadandtop)
# todo: 3.train from scratch


class QMainScreen(QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.mousePressEvent = self.scene_mousePressEvent
        self.ui.graphicsViewBoard.setScene(self.scene)
        self.ui.graphicsViewBoard.setFixedSize(499, 499)
        self.ui.actionNewGame.triggered.connect(self.startButton_click)
        self.ui.actionHint.triggered.connect(self.hint_toggle)
        self.ui.actionAI.triggered.connect(self.ai_toggle)
        self.ui.blackLcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.ui.whiteLcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        # self.ui.statusBar.hide()
        if platform.system() == 'Linux':
            self.setFixedSize(self.size())
        else:
            self.setFixedSize(600, 625)

        self.bg = ImageQt.ImageQt(Image.open('img/board2.png'))
        self.tatami = QImage('img/tatami.png').mirrored()
        palette = QPalette()
        # noinspection PyTypeChecker
        palette.setBrush(10, QBrush(self.tatami))
        self.setPalette(palette)

        self.repaint()

        self.newgame = QtWidgets.QMdiSubWindow()
        self.newgamewindow = Ui_NewGame()
        self.newgamewindow.setupUi(self.newgame)
        self.newgame.setFixedSize(self.newgame.size())
        self.newgamewindow.whichGameBox.currentIndexChanged.connect(self.whichGameChanged)
        self.newgamewindow.boardSizeBox_h.currentIndexChanged.connect(self.newwindow_boardsize_h)
        self.newgamewindow.boardSizeBox_w.currentIndexChanged.connect(self.newwindow_boardsize_w)
        self.newgamewindow.CancelButton.clicked.connect(self.cancelclick)
        self.newgamewindow.OKButton.clicked.connect(self.startgame)
        self.initiate_newgame()

        self.g = Og
        self.NNet = ONNet
        self.bsize = {6: [498, 83], 7: [497, 71], 8: [496, 62], 9: [495, 55], 10: [500, 50]}

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

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        f = 0 if platform.system() == 'Linux' else 20
        for i in range(1, 8):
            painter.fillRect(i+40, i+20+f, 520, 520, QtGui.QColor(10, 10, 10, int(40-1.25*i)))
        painter.fillRect(40, 20+f, 520, 520, QtGui.QColor(209, 143, 55))

    def fillshadow(self, x, y, side):
        for i in range(1, 4):
            rect = QtCore.QRectF(QtCore.QPointF(x * side-i+9, y * side-i+9), QtCore.QSizeF(side-10, side-10))
            self.scene.addEllipse(rect,
                                  QtGui.QPen(QtGui.QColor(0, 0, 0, int(30+10*i))),
                                  QtGui.QBrush(QtGui.QColor(0, 0, 0, int(30+10*i))))

    # -------------------------------- New Game -------------------------------- #
    def initiate_newgame(self):
        self.newgamewindow.whichGameBox.clear()
        self.newgamewindow.whichGameBox.addItem('Othello')
        self.newgamewindow.whichGameBox.addItem('Connect4')

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

    def cancelclick(self, _):
        self.newgame.hide()
    # ------------------------------ Main Window ------------------------------- #

    def ai_toggle(self, _):
        self.AI = not self.AI
        self.refresh()

    def updateText(self, ai=None, user=None):
        bfont = QFont()
        wfont = QFont()
        if self.g == Og:
            self.ui.blackLcdNumber.display(str(self.BLACK))
            self.ui.whiteLcdNumber.display(str(self.WHITE))
        else:
            pi, v = self.n1.predict(self.game.getCanonicalForm(self.board, self.b))
            self.ui.blackLcdNumber.display(str(int((v+1)*50)))
            self.ui.whiteLcdNumber.display(str(int(100-((v+1)*50))))
        if self.game.getGameEnded(self.board, self.turn):
            return

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
        if ai == -1:
            self.ui.rightPlayerLabel.setText('AI')
            self.ui.leftPlayerLabel.setText('Human')
        elif ai == 1:
            self.ui.leftPlayerLabel.setText('AI')
            self.ui.rightPlayerLabel.setText('Human')
        else:
            if user:
                self.ui.rightPlayerLabel.setText(user[1])
                self.ui.leftPlayerLabel.setText(user[0])
            else:
                self.ui.rightPlayerLabel.setText('Human')
                self.ui.leftPlayerLabel.setText('Human')
        if self.turn == self.b:
            bfont.setBold(True)
            bfont.setUnderline(True)
            self.ui.blackLabel.setFont(bfont)
            self.ui.whiteLabel.setFont(wfont)

        else:
            wfont.setBold(True)
            wfont.setUnderline(True)
            self.ui.blackLabel.setFont(bfont)
            self.ui.whiteLabel.setFont(wfont)

    def hint_toggle(self, _):
        self.hint = ~self.hint
        self.refresh()

    def startButton_click(self, _):
        self.newgame.show()

    def startgame(self, _):
        self.ui.graphicsViewBoard.resize(self.bsize[int(self.newgamewindow.boardSizeBox_w.currentText())][0],
                                         self.bsize[int(self.newgamewindow.boardSizeBox_h.currentText())][0])
        if self.newgamewindow.whichGameBox.currentIndex() == 0:
            self.g = Og
            self.NNet = ONNet
            self.game = self.g(int(self.newgamewindow.boardSizeBox_h.currentText()))
            self.n1 = self.NNet(self.game)
        elif self.newgamewindow.whichGameBox.currentIndex() == 1:
            self.g = Cg
            self.NNet = CNNet
            self.game = self.g(int(self.newgamewindow.boardSizeBox_h.currentText()),
                               int(self.newgamewindow.boardSizeBox_w.currentText()))
            self.n1 = self.NNet(self.game)
        weights = self.newgamewindow.weightBox.currentText()
        self.turn = 1
        self.board = self.game.getInitBoard()
        try:
            self.n1.load_checkpoint('ai/weights/', weights)
        except:
            print('Cannot load weights')
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
        self.updateText(ai=-self.turn)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        self.update()

    # noinspection PyArgumentList
    def scene_mousePressEvent(self, event):
        sidex = self.bsize[int(self.newgamewindow.boardSizeBox_w.currentText())][1]
        sidey = self.bsize[int(self.newgamewindow.boardSizeBox_h.currentText())][1]
        # self.auto()
        x = int(event.scenePos().x() // sidex)
        y = int(event.scenePos().y() // sidey)
        if self.g == Og or self.g == Gg:
            action = y * int(self.newgamewindow.boardSizeBox_w.currentText()) + x
        else:
            action = x
        valid = self.game.getValidMoves(self.board, self.turn)
        if valid[action] == 0:
            return

        self.board, self.turn = self.game.getNextState(self.board, self.turn, action)
        self.recentMove = [x, y, self.turn]
        self.refresh()
        self.updateText(self.turn)
        if self.ui.actionAI.isChecked() and self.game.getGameEnded(self.board, self.turn) == 0:
            QtTest.QTest.qWait(200)
            while True:
                self.aimove()
                valid = self.game.getValidMoves(self.board, self.turn)
                if np.sum(valid[:-1]) > 0 or self.game.getGameEnded(self.board, self.turn) != 0:
                    break
                else:
                    self.turn *= -1
                    QtTest.QTest.qWait(600)

    def auto(self):
        sidex = self.bsize[int(self.newgamewindow.boardSizeBox_w.currentText())][1]
        sidey = self.bsize[int(self.newgamewindow.boardSizeBox_h.currentText())][1]
        names = ['N22-C17', 'C17-N22', 'N34-C17', 'C17-N34', 'N22-C34', 'C34-N22', 'N34-C34', 'C34-N34']
        for idx, iteration in enumerate(names):
            os.mkdir(f'cap_3/{iteration}')
            ls = eval(open(f'moves_3/{idx+8}.txt', 'r').read())
            self.startgame(None)
            for i, action in enumerate(ls):
                action = int(action)
                self.board, self.turn = self.game.getNextState(self.board, self.turn, action)
                x = action % 8
                y = action // 8
                sr = QtCore.QRectF(QtCore.QPointF(x * sidex + (sidex/2)-7, y * sidey + (sidey/2) - 7),
                                   QtCore.QSizeF(14, 14))
                self.refresh()
                self.scene.addEllipse(sr, QtGui.QPen(QtCore.Qt.darkBlue), QtGui.QBrush(QtCore.Qt.blue))
                self.updateText(None, iteration.split('-'))
                QtTest.QTest.qWait(200)
                #
                im = self.grab()
                im.save(f'cap_3/{iteration}/{i}.jpg')
                #

    def aimove(self):
        action = self.mctsplayer(self.game.getCanonicalForm(self.board, self.turn))
        self.board, self.turn = self.game.getNextState(self.board, self.turn, action)
        self.recentMove = [action % int(self.newgamewindow.boardSizeBox_w.currentText()),
                           action // int(self.newgamewindow.boardSizeBox_h.currentText()),
                           self.turn]
        self.refresh()
        self.updateText(-self.turn)

    def refresh(self):
        self.scene.clear()
        pend = QtGui.QPen(QtGui.QColor(94, 46, 12))
        penl = QtGui.QPen(QtGui.QColor(209, 143, 55))
        pixMap = QtGui.QPixmap.fromImage(self.bg)
        self.scene.addPixmap(pixMap)
        sidex = self.bsize[int(self.newgamewindow.boardSizeBox_w.currentText())][1]
        sidey = self.bsize[int(self.newgamewindow.boardSizeBox_h.currentText())][1]
        self.WHITE = 0
        self.BLACK = 0
        for y in range(int(self.newgamewindow.boardSizeBox_h.currentText())):
            for x in range(int(self.newgamewindow.boardSizeBox_w.currentText())):
                if self.g == Og or self.g == Gg:
                    action = y * int(self.newgamewindow.boardSizeBox_h.currentText()) + x
                else:
                    action = x

                valid = self.game.getValidMoves(self.board, self.turn)
                rd = QtCore.QRectF(QtCore.QPointF(x * sidex, y * sidey), QtCore.QSizeF(sidex, sidey))
                rl = QtCore.QRectF(QtCore.QPointF(x * sidex+1, y * sidey+1), QtCore.QSizeF(sidex, sidey))
                sr = QtCore.QRectF(QtCore.QPointF(x * sidex + (sidex/2)-7, y * sidey + (sidey/2) - 7),
                                   QtCore.QSizeF(14, 14))
                self.scene.addRect(rd, pend)
                self.scene.addRect(rl, penl)
                if self.board[y][x] == self.b:
                    # self.fillshadow(x, y, side)
                    stone = QtSvg.QGraphicsSvgItem('img/stone_1.svg')
                    stone.setPos(x * sidex + 5, y * sidey + 5)
                    stone.setScale((min(sidex, sidey)-10)/43)
                    self.scene.addItem(stone)
                    self.BLACK += 1
                    # if [x, y, self.turn] == self.recentMove:
                    #     self.scene.addEllipse(sr, QtGui.QPen(QtCore.Qt.white), QtGui.QBrush(QtCore.Qt.white))
                elif self.board[y][x] == self.w:
                    # self.fillshadow(x, y, side)
                    # print(x * sidex + 5, y * sidey + 5)
                    # print(x, y)
                    stone = QtSvg.QGraphicsSvgItem('img/stone_-1.svg')
                    stone.setPos(x * sidex + 5, y * sidey + 5)
                    stone.setScale((min(sidex, sidey)-10)/43)
                    self.scene.addItem(stone)
                    self.WHITE += 1
                    # if [x, y, self.turn] == self.recentMove:
                    #     self.scene.addEllipse(sr, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.black))
                elif valid[action] == 1 and self.hint:
                    if self.newgamewindow.aiTurnBox.isChecked() or self.AI:
                        stone = QtSvg.QGraphicsSvgItem('img/stone_h0.svg')
                    elif self.turn == self.w:
                        stone = QtSvg.QGraphicsSvgItem('img/stone_h-1.svg')
                    else:
                        stone = QtSvg.QGraphicsSvgItem('img/stone_h1.svg')
                    stone.setPos(x * sidex + 20, y * sidey + 20)
                    stone.setScale(22/43)
                    self.scene.addItem(stone)
        self.update()
