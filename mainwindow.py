# -*- coding: utf-8 -*-
r"""
    Behold, removing tf.Session() in the very first line will cause "signal 11: SIGSEGV"
"""
import tensorflow as tf
tf.Session()
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

import numpy as np


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(841, 554)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.frame_2 = QtWidgets.QFrame(self.centralWidget)
        self.frame_2.setGeometry(QtCore.QRect(524, 12, 300, 501))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_2.setContentsMargins(12, 12, 12, 0)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonNewGame = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButtonNewGame.setObjectName("pushButtonNewGame")
        self.gridLayout.addWidget(self.pushButtonNewGame, 0, 0, 1, 2)
        self.pushButtonHintToggle = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButtonHintToggle.setObjectName("pushButtonHintToggle")
        self.pushButtonAIToggle = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButtonAIToggle.setObjectName("pushButtonAIToggle")
        self.gridLayout.addWidget(self.pushButtonHintToggle, 5, 0, 1, 2)
        self.gridLayout.addWidget(self.pushButtonAIToggle, 1, 0, 1, 2)
        self.label_w = QtWidgets.QLabel(self.groupBox_3)
        self.label_w.setObjectName("label_w")
        self.gridLayout.addWidget(self.label_w, 4, 0, 1, 1)
        self.lineEditNumMCTSSims = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditNumMCTSSims.setObjectName("lineEditTimeLimit")
        self.gridLayout.addWidget(self.lineEditNumMCTSSims, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.comboBoxWeightsName = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBoxWeightsName.setObjectName("comboBoxWeightsName")
        self.comboBoxWeightsName.addItem("")
        self.comboBoxWeightsName.addItem("")
        self.gridLayout.addWidget(self.comboBoxWeightsName, 4, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textEditInfo = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEditInfo.setObjectName("textEditInfo")
        self.verticalLayout_3.addWidget(self.textEditInfo)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.graphicsViewBoard = QtWidgets.QGraphicsView(self.centralWidget)
        self.graphicsViewBoard.setGeometry(QtCore.QRect(12, 12, 508, 508))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsViewBoard.sizePolicy().hasHeightForWidth())
        self.graphicsViewBoard.setSizePolicy(sizePolicy)
        self.graphicsViewBoard.setMaximumSize(QtCore.QSize(1000, 1000))
        self.graphicsViewBoard.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewBoard.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewBoard.setObjectName("graphicsViewBoard")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 841, 22))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Othello"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Game Options"))
        self.pushButtonNewGame.setText(_translate("MainWindow", "New Game"))
        self.pushButtonHintToggle.setText(_translate("MainWindow", "Hint Toggle"))
        self.pushButtonAIToggle.setText(_translate("MainWindow", "AI off"))
        self.label_w.setText(_translate("MainWindow", "AI at epoch"))
        self.label.setText(_translate("MainWindow", "numMCTSSims"))
        self.comboBoxWeightsName.setItemText(0, _translate("MainWindow", "60"))
        self.comboBoxWeightsName.setItemText(1, _translate("MainWindow", "73"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Game Info"))


r"""
    Since I was too lazy but prefer a pretty code.
    n: None, an empty square
    b: Black
    w: White
"""


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

        self.g = Og
        self.NNet = ONNet

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
        # weights = ['checkpoint_18.pth.tar', 'gobang_8x8x103.pth.tar']
        epch = self.ui.comboBoxWeightsName.currentIndex()
        self.turn = 1
        self.board = self.game.getInitBoard()
        n1.load_checkpoint('ai/weights/', weights[epch])
        try:
            nsims = int(self.ui.lineEditNumMCTSSims.text())
            self.args1 = dotdict({'numMCTSSims': nsims, 'cpuct': 1.0})
        except ValueError:
            self.args1 = dotdict({'numMCTSSims': 25, 'cpuct': 1.0})
        self.mcts1 = MCTS(self.game, self.n1, self.args1)
        self.mctsplayer = lambda x: np.argmax(self.mcts1.getActionProb(x, temp=0))

        self.refresh()
        if self.AI:
            self.scene.mousePressEvent(None)
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
        for x in range(8):
            for y in range(8):
                if self.g == Og or self.g == Gg:
                    action = x * 8 + y
                else:
                    action = x

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
