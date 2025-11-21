import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect
from main_window import MainWindow
from overlay_window import OverlayWindow
from popup_overlay import PopupOverlay
from window_capture import CaptureThread
from text_recognition import TextRecognizer
from translator import create_translator
from helpers import get_window_titles, get_window_rect

ocr = TextRecognizer()
sub_window = None
capture_thread = None
translator = create_translator("ollama")

def open_sub_window():
    global sub_window
    global capture_thread

    if sub_window is None:
        sub_window = PopupOverlay(main_window.selected_window, get_text_rects, translator.translate, get_window_rect)
        sub_window.show()
        capture_thread = CaptureThread(main_window.selected_window, ocr.recognize_text)
        capture_thread.start()

def close_sub_window():
    global sub_window
    global capture_thread

    if sub_window:
        capture_thread.stop()
        capture_thread = None
        sub_window.close()
        sub_window = None

def get_text_rects():
    res = ocr.results
    return [(text_box.text, QRect(text_box.x, text_box.y, text_box.w, text_box.h)) for text_box in res]

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow(get_window_titles)
    main_window.show()

    main_window.add_start_listener(open_sub_window)
    main_window.add_stop_listener(close_sub_window)

    sys.exit(app.exec())