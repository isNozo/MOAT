from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPainter, QColor, QCursor
from PySide6.QtCore import QPoint, Qt, Signal, Slot, QRunnable, QTimer, QObject, QThreadPool

class PopupOverlay(QWidget):
    def __init__(self, target_title, get_text_rects, process_text, get_window_rect):
        super().__init__()

        self.target_title = target_title
        self.get_text_rects = get_text_rects
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
        self.current_text_rect = None

        # Current task ID (for thread management)
        self.current_task_id = 0
        self.pool = QThreadPool()

    def update_overlay(self):
        # Update overlay window position
        rect = self.get_window_rect(self.target_title)
        if rect:
            self.setGeometry(*rect)

        # Calculate mouse position relative to the window
        global_pos = QCursor.pos()
        window_pos = self.geometry().topLeft()
        reletive_pos = global_pos - window_pos

        # Get text rectangles
        if self.in_any_rect:
            rects = [self.current_text_rect]
        else:
            rects = self.get_text_rects()

        # If the mouse is inside any rectangle
        for text, rect in rects:
            if rect.contains(reletive_pos):
                if not self.in_any_rect:
                    self.in_any_rect = True
                    self.current_text_rect = (text, rect)
                    self.startTextProcess(rect, text)
                return

        # If the mouse leaves the rectangle
        self.in_any_rect = False
        self.current_text_rect = None
        self.popup.hide()

        self.update()

    def startTextProcess(self, rect, text):
        # Show loading popup immediately
        self.updatePopup(rect, "Loading...")

        # Update task ID (ignore old results)
        self.current_task_id += 1

        # Start a separate thread for processing
        worker = TextProcessWorker(text, self.current_task_id, self.process_text)
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
        painter = QPainter(self)

        # Draw border around the overlay window
        painter.setPen(QColor(0, 170, 255))
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))

        # Draw text rectangles
        if self.enable_drawing_rect:
            rects = self.get_text_rects()
            for text, rect in rects:
                painter.fillRect(rect, QColor(255, 0, 0, 100))

class TextProcessWorker(QRunnable):
    def __init__(self, text, task_id, process_text):
        super().__init__()
        self.text = text
        self.task_id = task_id
        self.process_text = process_text
        self.signals = WorkerSignals()

    def run(self):
        result = self.process_text(self.text)
        self.signals.finished.emit(result, self.task_id)

class WorkerSignals(QObject):
    finished = Signal(str, int)