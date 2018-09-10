import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from mainscreen import QMainScreen


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QMainScreen()
    window.show()
    sys.exit(app.exec_())
