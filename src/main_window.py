from PySide6.QtWidgets import QWidget, QComboBox, QPushButton, QVBoxLayout
from PySide6.QtCore import Signal
import logging

logger = logging.getLogger(__name__)

class MainWindow(QWidget):
    def __init__(self, get_window_titles, on_start, on_stop):
        super().__init__()        

        self.get_window_titles = get_window_titles
        self.on_start = on_start
        self.on_stop = on_stop

        self.init_ui()

        logger.debug("initialized")

    def init_ui(self):
        self.setWindowTitle("MOAT - Mouse OCR & AI Translator")
        self.setFixedSize(240, 120)

        # Window selector
        self.window_selector = WindowSelector(self.get_window_titles)

        # Play/Stop toggle button
        self.toggle_btn = TogglePlayButton()
        self.toggle_btn.play.connect(lambda: self.on_start(self.window_selector.currentText()))
        self.toggle_btn.play.connect(lambda: self.window_selector.setEnabled(False))
        self.toggle_btn.stop.connect(self.on_stop)
        self.toggle_btn.stop.connect(lambda: self.window_selector.setEnabled(True))

        layout = QVBoxLayout()
        layout.addWidget(self.window_selector)
        layout.addWidget(self.toggle_btn)
        self.setLayout(layout)

    def closeEvent(self, event):
        logger.debug("closing")
        self.on_stop()
        super().closeEvent(event)


class WindowSelector(QComboBox):
    def __init__(self, get_window_titles):
        super().__init__()
        self.get_window_titles = get_window_titles

    def showPopup(self):
        self.refresh_window_list()
        super().showPopup()

    def refresh_window_list(self):
        selected_window = self.currentText()
        window_titles = self.get_window_titles()
        self.clear()
        self.addItems(window_titles)
        
        # Try to restore the previous selection if it still exists
        index = self.findText(selected_window)
        if index >= 0:
            self.setCurrentIndex(index)


class TogglePlayButton(QPushButton):
    play = Signal()
    stop = Signal()

    def __init__(self):
        super().__init__()

        self.button_style = """
            QPushButton {{
                font-size: 40px;
                height: 80px;
                background-color: {0};
                color: white;
                border-radius: 10px;
            }}
            QPushButton:pressed {{
                background-color: {1};
            }}
        """

        self.setCheckable(True)
        self.set_state_play()
        self.toggled.connect(self.update_state)

    def update_state(self, checked):
        if checked:
            self.set_state_stop()
            self.play.emit()
        else:
            self.set_state_play()
            self.stop.emit()

    def set_state_play(self):
        self.setText("▶")
        self.setStyleSheet(self.button_style.format("#3CB371", "#2E8B57"))

    def set_state_stop(self):
        self.setText("■")
        self.setStyleSheet(self.button_style.format("#CD5C5C", "#B24A4A"))