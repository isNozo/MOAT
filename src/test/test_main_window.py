import sys
import logging
from PySide6.QtWidgets import QApplication
from ..main_window import MainWindow
from ..helpers import get_window_titles

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)

    main_window = MainWindow(
        get_window_titles,
        lambda window_title: logging.info(f"Start called: {window_title}"),
        lambda: logging.info("Stop called")
    )
    main_window.show()

    sys.exit(app.exec())
