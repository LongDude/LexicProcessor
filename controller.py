import os

from PyQt6 import QtCore, QtWidgets, QtGui
from recources.view import Ui_MainWindow

class Controller(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Controller, self).__init__()
        self.setupUi(self)

        
