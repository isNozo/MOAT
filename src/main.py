import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from popup_overlay import PopupOverlay
from window_capture import CaptureThread
from text_recognition import TextRecognizer
from translator import TranslateWorkerManager
from helpers import get_window_titles, get_window_rect

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ocr = TextRecognizer()
    translator = TranslateWorkerManager()
    overlay_window = None
    capture_thread = None

    def get_text_rects():
        return ocr.results

    def start(window_title):
        global overlay_window
        global capture_thread

        if overlay_window is None:
            overlay_window = PopupOverlay(
                window_title,
                get_text_rects,
                translator.translate,
                get_window_rect
                )
            overlay_window.show()
            
            capture_thread = CaptureThread(
                window_title,
                ocr.recognize_text
                )
            capture_thread.start()

    def stop():
        global overlay_window
        global capture_thread
        
        if overlay_window:
            capture_thread.stop()
            capture_thread = None
            overlay_window.close()
            overlay_window = None

    main_window = MainWindow(get_window_titles, start, stop)
    main_window.show()

    sys.exit(app.exec())