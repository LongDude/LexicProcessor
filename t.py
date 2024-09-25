import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6 import QtWidgets

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button2 = QPushButton("Hello 2")
        central = QtWidgets.QWidget()
        HBox = QtWidgets.QHBoxLayout(central)
        HBox.addWidget(button)
        HBox.addWidget(button2)
        # Set the central widget of the Window.
        self.setCentralWidget(central)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()