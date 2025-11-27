from PySide6.QtWidgets import QApplication
import sys
import signal
from ..translator import TranslateWorkerManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = TranslateWorkerManager()

    def on_progress(result):
        print("Progress:", result)

    manager.translate("example", "This is an example sentence.", on_progress)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec())