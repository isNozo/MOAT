from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPainter, QColor, QCursor
from PySide6.QtCore import QPoint, Qt, Signal, Slot, QRunnable, QTimer, QObject, QThreadPool, QRect

class PopupOverlay(QWidget):
    def __init__(self, target_title, get_text_lines, process_text, get_window_rect):
        super().__init__()

        self.target_title = target_title
        self.get_text_lines = get_text_lines
        self.process_text = process_text
        self.get_window_rect = get_window_rect
        self.enable_drawing_rect = False

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
        
        # Set a timer to update the overlay window
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(1)

        # Popup label
        self.popup = QLabel("", self)
        self.popup.setStyleSheet(
            "background-color: yellow;"
            "border: 1px solid black;"
            "padding: 3px;"
        )
        self.popup.hide()
        self.in_any_rect = False
        self.current_textbox = None

        # Current task ID (for thread management)
        self.current_task_id = 0
        self.pool = QThreadPool()

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

    def startTextProcess(self, rect, word, full_text):
        # Show loading popup immediately
        self.updatePopup(rect, "Loading...")

        # Update task ID (ignore old results)
        self.current_task_id += 1

        # Start a separate thread for processing
        worker = TextProcessWorker(word, full_text, self.current_task_id, self.process_text)
        worker.signals.finished.connect(self.onWorkerFinished)
        self.pool.start(worker)

        self._pending_rect = rect  # Store rect for updating after processing

    # Called when the thread finishes
    @Slot(str, int)
    def onWorkerFinished(self, result_text, task_id):
        # Ignore old task results
        if task_id != self.current_task_id:
            return
        
        # If not in any rectangle, do nothing
        if self.in_any_rect is False:
            return

        # Update popup with the result
        self.updatePopup(self._pending_rect, result_text)

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

        # Draw text rectangles
        if self.enable_drawing_rect:
            lines = self.get_text_lines()
            for line in lines:
                for textbox in line:
                    rect = QRect(textbox.x/dpr, textbox.y/dpr, textbox.w/dpr, textbox.h/dpr)
                    painter.fillRect(rect, QColor(255, 0, 0, 100))

class TextProcessWorker(QRunnable):
    def __init__(self, word, full_text, task_id, process_text):
        super().__init__()
        self.word = word
        self.full_text = full_text
        self.task_id = task_id
        self.process_text = process_text
        self.signals = WorkerSignals()

    def run(self):
        result = self.process_text(self.word, self.full_text)
        self.signals.finished.emit(result, self.task_id)

class WorkerSignals(QObject):
    finished = Signal(str, int)