from PyQt6 import QtCore, QtGui, QtWidgets

class View(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
    
        self.setObjectName("Main Window")
        self.resize(1024, 720)
        self.setMinimumSize(256, 256)

        # central widget
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.hbox = QtWidgets.QHBoxLayout(self.centralWidget)

        self.menubar = QtWidgets.QMenuBar(self.centralWidget)
        self.setMenuBar(self.menubar)

        self.menubar.addAction("Save")
        self.menubar.addAction("Load")

        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.hbox.addWidget(self.textEdit)
        self.vbox = QtWidgets.QVBoxLayout(self.centralWidget)
        self.hbox.addLayout(self.vbox)
        self.lexicTree = QtWidgets.QTreeWidget(self.centralWidget)
        self.vbox.addWidget(self.lexicTree)

        self.analysisStats = QtWidgets.QTableWidget(self.centralWidget)
        self.analysisStats.setColumnCount(1)

        self.analysisStats.setRowCount(6)
        self.analysisStats.setVerticalHeaderLabels(["Идентификаторы:", "Комментарии:", "Операции:", "Ключевые слова:", "Литеры:", "Разделители:"])
        self.analysisStats.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.analysisStats.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

        for i in range(6):
            t2 = QtWidgets.QTableWidgetItem("0")
            self.analysisStats.setItem(i, 0, t2)
            
        self.analysisStats.setHorizontalHeaderLabels(["Количество"])
        self.analysisStats.horizontalHeader().setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.analysisStats.horizontalHeader().setHighlightSections(False)
        self.analysisStats.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.analysisStats.setEditTriggers(self.analysisStats.EditTrigger.NoEditTriggers)
        self.analysisStats.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.analysisStats.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.analysisStats.setShowGrid(False)

        self.lexicTree.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Expanding))
        self.lexicTree.setMaximumSize(200, 1900)
        self.prepare_tree()

        self.analysisStats.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,QtWidgets.QSizePolicy.Policy.Fixed))
        self.analysisStats.setMaximumSize(200, 600)
        self.analysisStats.setFixedSize(200, 210)
        self.analysisStats.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.vbox.addWidget(self.analysisStats)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Lexic Analyzer", "Lexic Analyzer"))

    def prepare_tree(self):
        self.lexicTree.setHeaderLabels(["Обнаруженные токены"])
        self.lexicTree.addTopLevelItems([QtWidgets.QTreeWidgetItem(None, [i]) for i in ["Идентификаторы", "Комментарии", "Операции", "Ключевые слова", "Литеры", "Разделители"]])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = View()
    ui.show()
    sys.exit(app.exec())