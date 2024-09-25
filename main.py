from controller import Controller
from PyQt6 import QtWidgets

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Controller()
    ui.show()
    sys.exit(app.exec())
