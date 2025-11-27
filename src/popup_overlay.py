from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPainter, QColor, QCursor
from PySide6.QtCore import QPoint, Qt, Signal, Slot, QRunnable, QTimer, QObject, QThreadPool, QRect
import ctypes

class PopupOverlay(QWidget):
    def __init__(self, target_title, get_text_lines, translate, get_window_rect):
        super().__init__()

        self.target_title = target_title
        self.get_text_lines = get_text_lines
        self.translate = translate
        self.get_window_rect = get_window_rect

        self.is_debug_mode = False
        self.is_block_mode = False
        self.prev_alt_state = False
        self.prev_q_state = False
        self.prev_d_state = False

        self.in_any_rect = False
        self.current_textbox = None

        # Set a frameless, always-on-top transparent window
        self.setWindowFlags(
            Qt.Window | 
            Qt.FramelessWindowHint |        # No window border
            Qt.WindowStaysOnTopHint |       # Always on top
            Qt.Tool                         # No taskbar icon
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Set a timer to update the overlay window
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_overlay)
        self.timer.timeout.connect(self.check_key_state)
        self.timer.start(1)

        # Popup label
        self.popup = QLabel("", self)
        self.popup.setStyleSheet(
            "background-color: yellow;"
            "border: 1px solid black;"
            "padding: 3px;"
        )
        self.popup.hide()

    def update_overlay(self):
        # Get device pixel ratio
        dpr = self.screen().devicePixelRatio()

        # Update overlay window position
        window_rect = self.get_window_rect(self.target_title)
        if window_rect:
            window_x = int(window_rect[0] / dpr)
            window_y = int(window_rect[1] / dpr)
            window_w = int(window_rect[2] / dpr)
            window_h = int(window_rect[3] / dpr)
            self.setGeometry(window_x, window_y, window_w, window_h)

        # Calculate mouse position relative to the window
        global_pos = QCursor.pos()
        window_pos = self.geometry().topLeft()
        reletive_pos = global_pos - window_pos

        # Get text rectangles
        if self.in_any_rect:
            lines = [[self.current_textbox]]
        else:
            lines = self.get_text_lines()

        # If the mouse is inside any rectangle
        for line in lines:
            for textbox in line:
                word = textbox.text
                word_rect = QRect(textbox.x/dpr, textbox.y/dpr, textbox.w/dpr, textbox.h/dpr)

                if(word == " "):
                    continue

                if word_rect.contains(reletive_pos):
                    if not self.in_any_rect:
                        self.in_any_rect = True
                        self.current_textbox = textbox

                        # Concatenate all texts in the line
                        full_line_text = ""
                        for tb in line:
                            full_line_text += tb.text

                        self.startTextProcess(word_rect, word, full_line_text)
                    return

        # If the mouse leaves the rectangle
        self.in_any_rect = False
        self.current_textbox = None
        self.popup.hide()

        self.update()

    def check_key_state(self):
        Key_Alt = 0x12
        Key_Q = 0x51
        Key_D = 0x44

        alt_pressed = ctypes.windll.user32.GetAsyncKeyState(Key_Alt) & 0x8000
        q_pressed = ctypes.windll.user32.GetAsyncKeyState(Key_Q) & 0x8000
        d_pressed = ctypes.windll.user32.GetAsyncKeyState(Key_D) & 0x8000

        # Alt+Q to toggle block mode
        if alt_pressed and q_pressed and not (self.prev_alt_state and self.prev_q_state):
            self.is_block_mode = not self.is_block_mode
        
        # Alt+D to toggle debug mode
        if alt_pressed and d_pressed and not (self.prev_alt_state and self.prev_d_state):
            self.is_debug_mode = not self.is_debug_mode
        
        self.prev_alt_state = alt_pressed
        self.prev_q_state = q_pressed
        self.prev_d_state = d_pressed
        
        self.update()

    def startTextProcess(self, rect, word, full_text):
        # Show loading popup immediately
        self.updatePopup(rect, "Loading...")

        # Start a separate thread for processing
        self.translate(word, full_text, self.onTranslationProgress)

        self._pending_rect = rect  # Store rect for updating after processing

    def onTranslationProgress(self, result_text):
        # If not in any rectangle, do nothing
        if self.in_any_rect is False:
            return

        # Update popup with the result
        self.updatePopup(self._pending_rect, result_text.strip())

    def updatePopup(self, rect, text):
        self.popup.setText(text)
        self.popup.adjustSize()

        # Calculate popup position
        popup_pos = QPoint()
        popup_pos.setX(rect.left() + (rect.width() - self.popup.width()) // 2)
        popup_pos.setY(rect.top() - self.popup.height() - 5)

        self.popup.move(popup_pos)
        self.popup.show()

    def paintEvent(self, event):
        # Get device pixel ratio
        dpr = self.screen().devicePixelRatio()

        painter = QPainter(self)

        # Draw border around the overlay window
        painter.setPen(QColor(0, 170, 255))
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))

        # Fill semi-transparent background in block mode
        if self.is_block_mode:
            painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        # Draw text rectangles
        if self.is_debug_mode:
            lines = self.get_text_lines()
            for line in lines:
                for textbox in line:
                    rect = QRect(textbox.x/dpr, textbox.y/dpr, textbox.w/dpr, textbox.h/dpr)
                    painter.fillRect(rect, QColor(255, 0, 0, 100))
