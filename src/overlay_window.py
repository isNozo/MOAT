from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QToolTip
from PySide6.QtCore import Qt, QTimer
from PySide6 import QtGui, QtCore
from PySide6.QtGui import QCursor
from helpers import get_window_rect

class OverlayWindow(QWidget):
    def __init__(self, target_title, translator):
        super().__init__()
        self.target_title = target_title
        self.results = []
        self.translator = translator
        
        # Set a frameless, always-on-top transparent window
        self.setWindowFlags(
            Qt.Window | 
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool |
            Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        # Resize the overlay window to match the target window
        rect = get_window_rect(self.target_title)
        if rect:
            self.setGeometry(*rect)
        else:
            # Default size if the target window is not found
            self.setGeometry(100, 100, 400, 300)

        # Set a timer to update the position of the overlay window
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)

        # Note: The label is not used for displaying text, but is required to create the QWidget
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        self.setLayout(layout)

    def update_position(self):
        rect = get_window_rect(self.target_title)
        if rect:
            self.setGeometry(*rect)

        # Global coordinates (position on the entire screen)
        global_pos = QCursor.pos()

        # Window's top-left position (in global coordinates)
        window_pos = self.geometry().topLeft()

        # Calculate relative position within the window
        self.relative_x = global_pos.x() - window_pos.x()
        self.relative_y = global_pos.y() - window_pos.y()

        self.update()

    def update_results(self, result):
        self.results = result
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Draw a border around the overlay window
        pen = QtGui.QPen(QtGui.QColor("#00AAFF"), 2)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))

        # Set pen for drawing
        pen = QtGui.QPen(QtGui.QColor(0, 255, 0, 200), 2)
        painter.setPen(pen)

        for textbox in self.results:
            # Calculate background rectangle
            bg_rect = QtCore.QRectF(
                textbox.x,
                textbox.y,
                textbox.w,
                textbox.h
            )
            
            # mouse over check
            if (self.relative_x >= textbox.x and self.relative_x <= textbox.x + textbox.w and
                self.relative_y >= textbox.y and self.relative_y <= textbox.y + textbox.h):
                text_bg = QtGui.QBrush(QtGui.QColor(255, 0, 0, 127))
                QToolTip.showText(QCursor.pos(), self.translator.translate(f"{textbox.text}"))
            else:
                text_bg = QtGui.QBrush(QtGui.QColor(0, 0, 0, 127))
            
            # Draw text background
            # painter.fillRect(bg_rect, text_bg)
