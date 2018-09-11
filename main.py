import sys
from PyQt5.QtWidgets import QApplication
from mainscreen import QMainScreen


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainScreen()
    window.show()
    sys.exit(app.exec_())
