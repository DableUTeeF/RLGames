from PyQt5 import QtCore, QtGui, Qt, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class MyMainScreen(QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()  # This is from a python export from QtDesigner
        self.ui.setupUi(self)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.red))
        painter.drawArc(QtCore.QRectF(250, 250, 10, 10), 0, 5760)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainscreen = MyMainScreen()
    mainscreen.show()
    app.exec_()
