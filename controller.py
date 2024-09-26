import os

from PyQt6 import QtCore, QtWidgets, QtGui
from recources.view import View

class Controller(View, QtWidgets.QMainWindow):
    
    
    def __init__(self):
        super(Controller, self).__init__()
        self.setupUi(self)
