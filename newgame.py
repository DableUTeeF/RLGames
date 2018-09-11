# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/newgame.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewGame(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 390)
        Form.setMinimumSize(QtCore.QSize(300, 390))
        Form.setMaximumSize(QtCore.QSize(300, 390))
        self.MainFrame = QtWidgets.QFrame(Form)
        self.MainFrame.setGeometry(QtCore.QRect(0, 0, 301, 391))
        self.MainFrame.setMinimumSize(QtCore.QSize(301, 391))
        self.MainFrame.setMaximumSize(QtCore.QSize(301, 391))
        self.MainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MainFrame.setObjectName("MainFrame")
        self.DecissionButtonsFrame = QtWidgets.QFrame(self.MainFrame)
        self.DecissionButtonsFrame.setGeometry(QtCore.QRect(100, 330, 171, 41))
        self.DecissionButtonsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.DecissionButtonsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.DecissionButtonsFrame.setObjectName("DecissionButtonsFrame")
        self.OKButton = QtWidgets.QPushButton(self.DecissionButtonsFrame)
        self.OKButton.setGeometry(QtCore.QRect(10, 10, 51, 25))
        self.OKButton.setObjectName("OKButton")
        self.CancleButton = QtWidgets.QPushButton(self.DecissionButtonsFrame)
        self.CancleButton.setGeometry(QtCore.QRect(70, 10, 89, 25))
        self.CancleButton.setObjectName("CancleButton")
        self.ObjectFrame = QtWidgets.QFrame(self.MainFrame)
        self.ObjectFrame.setGeometry(QtCore.QRect(30, 30, 241, 291))
        self.ObjectFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ObjectFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ObjectFrame.setObjectName("ObjectFrame")
        self.whichGameLabel = QtWidgets.QLabel(self.ObjectFrame)
        self.whichGameLabel.setGeometry(QtCore.QRect(20, 40, 67, 17))
        self.whichGameLabel.setObjectName("whichGameLabel")
        self.whichGameBox = QtWidgets.QComboBox(self.ObjectFrame)
        self.whichGameBox.setGeometry(QtCore.QRect(120, 40, 91, 25))
        self.whichGameBox.setObjectName("whichGameBox")
        self.boardSizeLabel = QtWidgets.QLabel(self.ObjectFrame)
        self.boardSizeLabel.setGeometry(QtCore.QRect(20, 90, 67, 17))
        self.boardSizeLabel.setObjectName("boardSizeLabel")
        self.boardSizeBox_w = QtWidgets.QComboBox(self.ObjectFrame)
        self.boardSizeBox_w.setGeometry(QtCore.QRect(120, 90, 41, 25))
        self.boardSizeBox_w.setObjectName("boardSizeBox_w")
        self.mctsSimsLabel = QtWidgets.QLabel(self.ObjectFrame)
        self.mctsSimsLabel.setGeometry(QtCore.QRect(20, 140, 71, 17))
        self.mctsSimsLabel.setObjectName("mctsSimsLabel")
        self.weightLabel = QtWidgets.QLabel(self.ObjectFrame)
        self.weightLabel.setGeometry(QtCore.QRect(20, 190, 67, 17))
        self.weightLabel.setObjectName("weightLabel")
        self.weightBox = QtWidgets.QComboBox(self.ObjectFrame)
        self.weightBox.setGeometry(QtCore.QRect(120, 190, 91, 25))
        self.weightBox.setObjectName("weightBox")
        self.aiTurnLabel = QtWidgets.QLabel(self.ObjectFrame)
        self.aiTurnLabel.setGeometry(QtCore.QRect(20, 240, 67, 17))
        self.aiTurnLabel.setObjectName("aiTurnLabel")
        self.aiTurnBox = QtWidgets.QCheckBox(self.ObjectFrame)
        self.aiTurnBox.setGeometry(QtCore.QRect(120, 240, 92, 23))
        self.aiTurnBox.setText("")
        self.aiTurnBox.setObjectName("aiTurnBox")
        self.mctsSimsBox = QtWidgets.QSpinBox(self.ObjectFrame)
        self.mctsSimsBox.setGeometry(QtCore.QRect(120, 140, 48, 26))
        self.mctsSimsBox.setMinimum(2)
        self.mctsSimsBox.setMaximum(100)
        self.mctsSimsBox.setValue(25)
        self.mctsSimsBox.setObjectName("mctsSimsBox")
        self.boardSizeBox_h = QtWidgets.QComboBox(self.ObjectFrame)
        self.boardSizeBox_h.setGeometry(QtCore.QRect(170, 90, 41, 25))
        self.boardSizeBox_h.setObjectName("boardSizeBox_h")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "New Game"))
        self.OKButton.setText(_translate("Form", "OK"))
        self.CancleButton.setText(_translate("Form", "cancle"))
        self.whichGameLabel.setText(_translate("Form", "game"))
        self.boardSizeLabel.setText(_translate("Form", "boardSize"))
        self.mctsSimsLabel.setText(_translate("Form", "MCTSSims"))
        self.weightLabel.setText(_translate("Form", "weight"))
        self.aiTurnLabel.setText(_translate("Form", "AI first"))

