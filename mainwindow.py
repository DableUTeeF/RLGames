# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(600, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
        self.graphicsViewBoard = QtWidgets.QGraphicsView(self.centralWidget)
        self.graphicsViewBoard.setGeometry(QtCore.QRect(50, 40, 500, 500))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsViewBoard.sizePolicy().hasHeightForWidth())
        self.graphicsViewBoard.setSizePolicy(sizePolicy)
        self.graphicsViewBoard.setMaximumSize(QtCore.QSize(1000, 1000))
        self.graphicsViewBoard.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewBoard.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsViewBoard.setObjectName("graphicsViewBoard")
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setGeometry(QtCore.QRect(50, 550, 501, 45))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.whiteLcdNumber = QtWidgets.QLCDNumber(self.frame)
        self.whiteLcdNumber.setGeometry(QtCore.QRect(400, 0, 40, 40))
        self.whiteLcdNumber.setDigitCount(2)
        self.whiteLcdNumber.setObjectName("whiteLcdNumber")
        self.whiteLabel = QtWidgets.QLabel(self.frame)
        self.whiteLabel.setGeometry(QtCore.QRect(450, 10, 41, 23))
        self.whiteLabel.setObjectName("whiteLabel")
        self.blackLabel = QtWidgets.QLabel(self.frame)
        self.blackLabel.setGeometry(QtCore.QRect(10, 10, 67, 23))
        self.blackLabel.setObjectName("blackLabel")
        self.blackLcdNumber = QtWidgets.QLCDNumber(self.frame)
        self.blackLcdNumber.setGeometry(QtCore.QRect(50, 0, 40, 40))
        self.blackLcdNumber.setDigitCount(2)
        self.blackLcdNumber.setObjectName("blackLcdNumber")
        self.rightPlayerLabel = QtWidgets.QLabel(self.frame)
        self.rightPlayerLabel.setGeometry(QtCore.QRect(330, 10, 60, 23))
        self.rightPlayerLabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rightPlayerLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.rightPlayerLabel.setObjectName("rightPlayerLabel")
        self.leftPlayerLabel = QtWidgets.QLabel(self.frame)
        self.leftPlayerLabel.setGeometry(QtCore.QRect(100, 10, 67, 23))
        self.leftPlayerLabel.setObjectName("leftPlayerLabel")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 600, 22))
        self.menuBar.setMinimumSize(QtCore.QSize(10, 10))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionNew_Game = QtWidgets.QAction(MainWindow)
        self.actionNew_Game.setObjectName("actionNew_Game")
        self.actionNewGame = QtWidgets.QAction(MainWindow)
        self.actionNewGame.setObjectName("actionNewGame")
        self.actionAI = QtWidgets.QAction(MainWindow)
        self.actionAI.setCheckable(True)
        self.actionAI.setChecked(True)
        self.actionAI.setObjectName("actionAI")
        self.actionHint = QtWidgets.QAction(MainWindow)
        self.actionHint.setCheckable(True)
        self.actionHint.setChecked(False)
        self.actionHint.setObjectName("actionHint")
        self.menuFile.addAction(self.actionNewGame)
        self.menuFile.addAction(self.actionAI)
        self.menuFile.addAction(self.actionHint)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Othello"))
        self.whiteLabel.setText(_translate("MainWindow", "White"))
        self.blackLabel.setText(_translate("MainWindow", "Black"))
        self.rightPlayerLabel.setText(_translate("MainWindow", "AI"))
        self.leftPlayerLabel.setText(_translate("MainWindow", "Human"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew_Game.setText(_translate("MainWindow", "New Game"))
        self.actionNewGame.setText(_translate("MainWindow", "New Game"))
        self.actionAI.setText(_translate("MainWindow", "AI"))
        self.actionHint.setText(_translate("MainWindow", "Hint"))

