import sys
import signal
import random
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect
from ..popup_overlay import PopupOverlay

def get_text_rects():
    rect_list = []
    random.seed(0)
    
    for i in range(8):
        x = random.randint(20, 400)
        y = random.randint(20, 300)
        w = random.randint(40, 120)
        h = random.randint(30, 100)
        text = f"Rect {i}"
        rect_list.append((text, QRect(x, y, w, h)))

    return rect_list

def process_text(text):
    random.seed(None)
    sleep_time = random.uniform(0.1, 0.5)
    time.sleep(sleep_time)
    return f"[Processed] {text}, took {sleep_time:.2f}s"

def get_window_rect(title):
    return (500, 500, 500, 400)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = PopupOverlay("dummy", get_text_rects, process_text, get_window_rect)
    w.enable_drawing_rect = True
    w.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec())
