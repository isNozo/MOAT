import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect, Qt, QPoint

def get_rects():
    rect_list = []
    random.seed(0)
    
    for i in range(6):
        x = random.randint(20, 400)
        y = random.randint(20, 300)
        w = random.randint(40, 120)
        h = random.randint(30, 100)
        text = f"Rect {i}"
        rect_list.append((text, QRect(x, y, w, h)))

    return rect_list


class HoverPopupWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self.popup = QLabel("", self)
        self.popup.setStyleSheet(
            "background-color: yellow;"
            "border: 1px solid black;"
            "padding: 3px;"
        )
        self.popup.hide()

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        rects = get_rects()

        in_any_rect = False

        for text, rect in rects:
            if rect.contains(pos):
                in_any_rect = True
                self.updatePopup(rect, text)
                break

        if not in_any_rect:
            self.popup.hide()

    def updatePopup(self, rect, text):
        self.popup.setText(text)
        self.popup.adjustSize()

        popup_pos = QPoint()
        popup_pos.setX(rect.left() + (rect.width() - self.popup.width()) // 2)
        popup_pos.setY(rect.top() - self.popup.height() - 5)

        self.popup.move(popup_pos)
        self.popup.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        colors = [QColor(200, 200, 255), QColor(200, 255, 200), QColor(255, 200, 200)]

        rects = get_rects()
        for i, (text, rect) in enumerate(rects):
            painter.setBrush(colors[i % len(colors)])
            painter.drawRect(rect)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = HoverPopupWidget()
    w.resize(450, 320)
    w.show()
    sys.exit(app.exec())
