from PyQt6 import QtCore, QtGui, QtWidgets

class View(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("Main Window")
        self.resize(1024, 1024)
        self.setMinimumSize(256, 256)

        self.centralWidget = QtWidgets.QWidget(parent=self)
        self.setObjectName("centralWidget")
        self.hbox = QtWidgets.QHBoxLayout(self.centralWidget) 
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setContentsMargins(0, 0, 0, 0)
        # self.HBox1 = 
        # self.HBox1.setObjectName("HBox 1")
        # self.HBox1.setContentsMargins(0, 0, 0, 0)



        # # Text edit
        self.btn1 = QtWidgets.QPushButton(text="1")
        self.hbox.addWidget(self.btn1)
        self.btn2 = QtWidgets.QPushButton()
        self.hbox.addWidget(self.btn2)
        self.btn3 = QtWidgets.QPushButton()
        self.hbox.addWidget(self.btn3)
        # Information widget
        # self.VBox2 = QtWidgets.QVBoxLayout(self.centralWidget)
        # self.HBox1.addChildLayout(self.VBox2)

        # All found tokens (list, grouping and adresses)
        # self.tokensTree = QtWidgets.QTreeWidget(self.centralWidget)
        # self.VBox2.addChildWidget(self.tokensTree)

        # Counting different lexem types
        # self.resTable = QtWidgets.QTableView(self.centralWidget)
        # self.VBox2.addChildWidget(self.resTable)


        # self.tokensTree.setHeaderLabel("Hello")
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Lexic Analyzer", "Lexic Analyzer"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = View()
    ui.show()
    sys.exit(app.exec())