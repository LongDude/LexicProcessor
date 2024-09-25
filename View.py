import PyQt6 as qt
import PyQt6.QtCore as qc
import PyQt6.QtWidgets as qw
import PyQt6.QtGui as qg
import typing


class QFrameProxyFocus(qw.QFrame):
    """ Наследие борьбы за проброску ивентов мышки """
    got_focus = qc.pyqtSignal()
    lost_focus = qc.pyqtSignal()

    def focusInEvent(self, a0: typing.Optional[qg.QFocusEvent]) -> None:
        self.got_focus.emit()
        super(QFrameProxyFocus, self).focusInEvent(a0)

    def focusOutEvent(self, a0: typing.Optional[qg.QFocusEvent]) -> None:
        self.lost_focus.emit()
        super(QFrameProxyFocus, self).focusInEvent(a0)


class View(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Main initialization
        self.setObjectName("MainWindow")
        self.resize(1024, 720)
        self.setMinimumSize(225, 225)

        # Font
        font = qg.QFont()
        font.setFamily("Iosevka")
        font.setPointSize(14)
        
        # Central widget
        self.graphic_layer_widget = qw.QWidget(parent=self)
        self.graphic_layer_widget.setStyleSheet("border: 0")

        # Statusbar
        self.statusbar = qw.QStatusBar(parent=self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # Graphics view (for image)
        self.graphic_layout = qw.QVBoxLayout(self.graphic_layer_widget)
        self.graphic_layout.setContentsMargins(0, 0, 0, 0)
        self.graphicView = qw.QGraphicsView(parent=self.graphic_layer_widget)
        self.graphicView.setGeometry(self.geometry())
        self.graphicView.setAlignment(qc.Qt.AlignmentFlag.AlignCenter)
        self.graphic_layout.addWidget(self.graphicView)
        self.graphicView.setContentsMargins(5, 5, 5, 5)
        self.graphicView.setHorizontalScrollBarPolicy(qt.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicView.setVerticalScrollBarPolicy(qt.QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Button layer (overlapping widget, size manually updated to screen size)
        #self.button_layer_widget = qw.QWidget(parent=self)
        #self.button_layer_widget.setAttribute(qc.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        # Vertical layout for rows
        #self.button_vertical_layout = qw.QVBoxLayout(self.button_layer_widget)

        # For open|save buttons
        #self.filemenu_layout = qw.QHBoxLayout(self.button_layer_widget)
        #self.button_vertical_layout.addLayout(self.filemenu_layout)

        # Open\load frame
        #self.file_frame = QFrameProxyFocus(parent=self.button_layer_widget)
        self.file_frame = qw.QFrame(self)
        self.file_frame.setObjectName("file_frame")
        #self.file_frame.got_focus.connect(lambda:  self.button_layer_widget.setAttribute(qc.Qt.WidgetAttribute.WA_TransparentForMouseEvents, False))
        #self.file_frame.lost_focus.connect(lambda:  self.button_layer_widget.setAttribute(qc.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True))
        #self.filemenu_layout.addWidget(self.file_frame)

        # Layout for fileworks buttons
        self.file_frame_layout = qw.QHBoxLayout(self.file_frame)
        self.file_frame_layout.setContentsMargins(4, 4, 4, 4)
        #filehsplitter = qw.QSpacerItem(40, 20, qw.QSizePolicy.Policy.Expanding, qw.QSizePolicy.Policy.Minimum)
        #self.filemenu_layout.addItem(filehsplitter)

        self.but_open = qw.QPushButton(self.file_frame)
        self.but_open.setObjectName("button_open")
        self.but_open.setText("Open")
        self.but_open.setFixedSize(32, 20)
        self.file_frame_layout.addWidget(self.but_open)

        self.file_buttons_vline = qw.QFrame(parent=self.file_frame)
        self.file_buttons_vline.setFrameShape(qw.QFrame.Shape.VLine)
        self.file_buttons_vline.setFrameShadow(qw.QFrame.Shadow.Plain)
        self.file_buttons_vline.setObjectName("vline")
        self.file_buttons_vline.setFixedSize(2, 20)
        self.file_frame_layout.addWidget(self.file_buttons_vline)

        self.but_save = qw.QPushButton(self.file_frame)
        self.but_save.setObjectName("button_save")
        self.but_save.setText("Save")
        self.but_save.setFixedSize(32, 20)
        self.file_frame_layout.addWidget(self.but_save)
        # ----

        # Vertical spacer
        #vspacer = qw.QSpacerItem(20, 40, qw.QSizePolicy.Policy.Minimum, qw.QSizePolicy.Policy.Expanding)
        #self.button_vertical_layout.addItem(vspacer)
        
        # Horizontal row, 'dock' to window`s bottom
        #self.button_row = qw.QHBoxLayout(self.button_layer_widget)

        # Left spacer
        #spacer_left = qw.QSpacerItem(40, 20, qw.QSizePolicy.Policy.Expanding, qw.QSizePolicy.Policy.Minimum)
        #self.button_row.addItem(spacer_left)

        # Panel for buttons
        #self.buttonFrame = qw.QFrame(self.button_layer_widget)
        self.buttonFrame = qw.QFrame(self)
        self.buttonFrame.setObjectName("buttonFrame")
        #self.button_row.addWidget(self.buttonFrame)

        # Buttons collection
        self.buttons_layout = qw.QHBoxLayout(self.buttonFrame)
        self.buttons_layout.setContentsMargins(4, 4, 4, 4)

        # Center image
        self.but_center = qw.QPushButton(parent=self.buttonFrame)
        self.but_center.setFixedSize(32, 32)
        icon_center = qg.QIcon()
        icon_center.addPixmap(qg.QPixmap("Icons/focus.png"), qg.QIcon.Mode.Normal, qg.QIcon.State.Off)
        self.but_center.setIcon(icon_center)
        self.but_center.setIconSize(qc.QSize(32, 32))
        self.buttons_layout.addWidget(self.but_center)

        # Zoom in image
        self.but_zoom_in = qw.QPushButton(parent=self.buttonFrame)
        self.but_zoom_in.setFixedSize(32, 32)
        icon_zoom_in = qg.QIcon()
        icon_zoom_in.addPixmap(qg.QPixmap("Icons/zoom-in.png"),qg.QIcon.Mode.Normal, qg.QIcon.State.Off)
        self.but_zoom_in.setIcon(icon_zoom_in)
        self.but_zoom_in.setIconSize(qc.QSize(32, 32))
        self.buttons_layout.addWidget(self.but_zoom_in)

        # Zoom out image
        self.but_zoom_out = qw.QPushButton(parent=self.buttonFrame)
        self.but_zoom_out.setFixedSize(32, 32)
        icon_zoom_out = qg.QIcon()
        icon_zoom_out.addPixmap(qg.QPixmap("Icons/magnifying-glass.png"), qg.QIcon.Mode.Normal, qg.QIcon.State.Off)
        self.but_zoom_out.setIcon(icon_zoom_out)
        self.but_zoom_out.setIconSize(qc.QSize(32, 32))
        self.buttons_layout.addWidget(self.but_zoom_out)

        # Rotate image left
        self.but_rotate_left = qw.QPushButton(parent=self.buttonFrame)
        self.but_rotate_left.setFixedSize(32, 32)
        icon_rotate_left = qg.QIcon()
        icon_rotate_left.addPixmap(qg.QPixmap("Icons/rotate_counter_clockwise.png"), qg.QIcon.Mode.Normal, qg.QIcon.State.Off)
        self.but_rotate_left.setIcon(icon_rotate_left)
        self.but_rotate_left.setIconSize(qc.QSize(32, 32))
        self.buttons_layout.addWidget(self.but_rotate_left)

        # Rotate image right
        self.but_rotate_right = qw.QPushButton(parent=self.buttonFrame)
        self.but_rotate_right.setFixedSize(32, 32)
        icon_rotate_right = qg.QIcon()
        icon_rotate_right.addPixmap(qg.QPixmap("Icons/rotate_clockwise.png"), qg.QIcon.Mode.Normal, qg.QIcon.State.Off)
        self.but_rotate_right.setIcon(icon_rotate_right)
        self.but_rotate_right.setIconSize(qc.QSize(32, 32))
        self.buttons_layout.addWidget(self.but_rotate_right)

        # Mirror image
        self.but_mirror = qw.QPushButton(parent=self.buttonFrame)
        self.but_mirror.setFixedSize(32, 32)
        icon_mirror_image = qg.QIcon()
        icon_mirror_image.addPixmap(qg.QPixmap("Icons/flip.png"), qg.QIcon.Mode.Normal, qg.QIcon.State.Off)
        self.but_mirror.setIcon(icon_mirror_image)
        self.but_mirror.setIconSize(qc.QSize(32, 32))
        self.buttons_layout.addWidget(self.but_mirror)

        # Right spacer
        #spacer_right = qw.QSpacerItem(40, 20, qw.QSizePolicy.Policy.Expanding, qw.QSizePolicy.Policy.Minimum)
        #self.button_row.addItem(spacer_right)

        # Adding row to layout
        #self.button_vertical_layout.addLayout(self.button_row)

        # Finishing
        self.setCentralWidget(self.graphic_layer_widget)
        #self.button_layer_widget.setGeometry(10, 10, self.size().width() - 20, self.size().height() - 30)

        _translate = qc.QCoreApplication.translate
        self.setWindowTitle(_translate("Image Viewer", "Image Viewer"))

        try:
            f = open("./Recources/stylesheet.css", "r")
            self.setStyleSheet(f.read())
            f.close()
        except Exception as e:
            print(e)

        # Stylesheets!
        #self.graphicView.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        #self.buttonFrame.setStyleSheet("QFrame {border-width: 0px; border-style: solid; border-radius: 7px; background-color: rgb(125, 207, 230);} QPushButton:pressed{background-color: rgb(126, 126, 126);}")
        #self.but_center.setStyleSheet("QPushButton:pressed{background-color: rgb(126, 126, 126);}")

    def resizeEvent(self, a0: typing.Optional[qg.QResizeEvent]) -> None:
        # self.button_layer_widget.setGeometry(0, 0, self.size().width(), self.size().height() - 20)
        qw.QMainWindow.resizeEvent(self, a0)
        self.buttonFrame.setGeometry(
            self.size().width() // 2 - 110,
            self.size().height() - 70,
            220,
            40
        )
        self.file_frame.setGeometry(
            10,
            10,
            86,
            28
        )


if __name__ == '__main__':
    import sys
    app = qw.QApplication(sys.argv)
    ui = View()
    ui.show()
    sys.exit(app.exec())
