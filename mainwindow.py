# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow
from ai.othello.OthelloGame import OthelloGame


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
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEditTimeLimit = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditTimeLimit.setObjectName("lineEditTimeLimit")
        self.gridLayout.addWidget(self.lineEditTimeLimit, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.comboBoxNumberOfHumans = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBoxNumberOfHumans.setObjectName("comboBoxNumberOfHumans")
        self.comboBoxNumberOfHumans.addItem("")
        self.comboBoxNumberOfHumans.addItem("")
        self.gridLayout.addWidget(self.comboBoxNumberOfHumans, 2, 1, 1, 1)
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
        self.groupBox = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEditEvents = QtWidgets.QTextEdit(self.groupBox)
        self.textEditEvents.setObjectName("textEditEvents")
        self.verticalLayout.addWidget(self.textEditEvents)
        self.verticalLayout_2.addWidget(self.groupBox)
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
        self.label_2.setText(_translate("MainWindow", "Human Players"))
        self.label.setText(_translate("MainWindow", "Time Limit (sec)"))
        self.comboBoxNumberOfHumans.setItemText(0, _translate("MainWindow", "1"))
        self.comboBoxNumberOfHumans.setItemText(1, _translate("MainWindow", "2"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Game Info"))
        self.groupBox.setTitle(_translate("MainWindow", "Game Events"))


r"""
    Since I was too lazy but prefer a pretty code.
    n: None, an empty square
    b: Black
    w: White
"""
n = None
b = 0
w = 1
pieces = [[n, n, n, n, n, n, n, n],
          [n, n, n, n, n, n, n, n],
          [n, n, n, n, n, n, n, n],
          [n, n, n, w, b, n, n, n],
          [n, n, n, b, w, n, n, n],
          [n, n, n, n, n, n, n, n],
          [n, n, n, n, n, n, n, n],
          [n, n, n, n, n, n, n, n]]

r"""
    False is 0 which mean False == black, True == white
"""
turn = False

r"""
    A game to play and somehow, contain the state
"""
game = None


class QMainScreen(QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()  # This is from a python export from QtDesigner
        self.ui.setupUi(self)
        self.scene = graphicsScene()
        self.ui.graphicsViewBoard.setScene(self.scene)
        self.ui.pushButtonNewGame.clicked.connect(self.startButton_click)

    def startButton_click(self):
        global pieces, game
        game = OthelloGame(8)
        pieces = [[n, n, n, n, n, n, n, n],
                  [n, n, n, n, n, n, n, n],
                  [n, n, n, n, n, n, n, n],
                  [n, n, n, w, b, n, n, n],
                  [n, n, n, b, w, n, n, n],
                  [n, n, n, n, n, n, n, n],
                  [n, n, n, n, n, n, n, n],
                  [n, n, n, n, n, n, n, n]]
        pen = QtGui.QPen(QtCore.Qt.black)
        side = 62
        for i in range(8):
            for j in range(8):
                r = QtCore.QRectF(QtCore.QPointF(i * side, j * side), QtCore.QSizeF(side, side))
                pr = QtCore.QRectF(QtCore.QPointF(i * side + 5, j * side + 5), QtCore.QSizeF(side - 10, side - 10))
                self.scene.addRect(r, pen, QtGui.QBrush(QtCore.Qt.darkGreen))
                if pieces[i][j] == b:
                    self.scene.addEllipse(pr, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.black))
                elif pieces[i][j] == w:
                    self.scene.addEllipse(pr, QtGui.QPen(QtCore.Qt.white), QtGui.QBrush(QtCore.Qt.white))

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        self.update()


class graphicsScene(QtWidgets.QGraphicsScene):
    r"""
        Since the original QGraphicsScene doesn't has the mouseEvent implemented, so I need to
        reconstruct a new class
    """

    def __init__(self, parent=None):
        super(graphicsScene, self).__init__(parent)

    def mouseReleaseEvent(self, event):
        self.update()

    def mousePressEvent(self, event):
        global pieces, turn, game
        x = int(event.scenePos().x() // 62)
        y = int(event.scenePos().y() // 62)
        pr = QtCore.QRectF(QtCore.QPointF(x*62+5, y*62+5), QtCore.QSizeF(52, 52))
        pieces[x][y] = turn
        if ~turn:
            self.addEllipse(pr, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.black))
        else:
            self.addEllipse(pr, QtGui.QPen(QtCore.Qt.white), QtGui.QBrush(QtCore.Qt.white))
        turn = ~turn
        self.update()
