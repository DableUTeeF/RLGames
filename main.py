import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from mainwindow import Ui_MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.setupUi(window)
    window.show()
    sys.exit(app.exec_())
