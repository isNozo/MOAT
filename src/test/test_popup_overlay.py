import sys
import signal
import random
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect
from ..popup_overlay import PopupOverlay
from ..helpers import get_window_titles, get_window_rect

def get_text_rects():
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

def process_text(text):
    time.sleep(0.5)
    return f"[Processed] {text}"


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # List available window titles
    window_titles = get_window_titles()
    print("Available window titles:")
    for i, title in enumerate(window_titles):
        print(f"{i}: {title}")
    
    # Select a window to capture
    selected_index = int(input("Enter the number of the window to capture: "))
    selected_window = window_titles[selected_index]

    w = PopupOverlay(selected_window, get_text_rects, process_text, get_window_rect)
    w.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec())
