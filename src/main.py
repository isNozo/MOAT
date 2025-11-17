import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from overlay_window import OverlayWindow
from window_capture import CaptureThread
from text_recognition import TextRecognizer
from translator import create_translator
from helpers import get_window_titles

sub_window = None
capture_thread = None
translator = create_translator("argos")

def open_sub_window():
    global sub_window
    global capture_thread

    if sub_window is None:
        sub_window = OverlayWindow(main_window.selected_window, translator)
        sub_window.show()
        capture_thread = CaptureThread(main_window.selected_window, process_frame)
        capture_thread.start()

def close_sub_window():
    global sub_window
    global capture_thread

    if sub_window:
        capture_thread.stop()
        capture_thread = None
        sub_window.close()
        sub_window = None

def process_frame(frame_buffer):
    """Process captured frame"""
    result = ocr.recognize_text(frame_buffer)
    
    if result is not None:
        sub_window.update_results(result)

if __name__ == "__main__":
    ocr = TextRecognizer()
    app = QApplication(sys.argv)

    main_window = MainWindow(get_window_titles)
    main_window.show()

    main_window.add_start_listener(open_sub_window)
    main_window.add_stop_listener(close_sub_window)

    sys.exit(app.exec())