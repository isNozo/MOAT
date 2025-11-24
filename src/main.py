import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from popup_overlay import PopupOverlay
from window_capture import CaptureThread
from text_recognition import TextRecognizer
from translator import create_translator
from helpers import get_window_titles, get_window_rect

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ocr = TextRecognizer()
    translator = create_translator("ollama")
    overlay_window = None
    capture_thread = None

    main_window = MainWindow(get_window_titles)
    main_window.show()

    def get_text_rects():
        return ocr.results

    def start():
        global overlay_window
        global capture_thread

        if overlay_window is None:
            overlay_window = PopupOverlay(
                main_window.selected_window,
                get_text_rects,
                translator.translate,
                get_window_rect
                )
            overlay_window.show()
            
            capture_thread = CaptureThread(
                main_window.selected_window,
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

    main_window.add_start_listener(start)
    main_window.add_stop_listener(stop)

    sys.exit(app.exec())