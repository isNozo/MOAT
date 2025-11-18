from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QDialog
)
from PySide6.QtCore import Qt, QPoint

class BalloonPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.drag_pos = None  # ドラッグ位置保存

        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet("""
            QWidget#wrapper {
                background: white;
                border: 1px solid #888;
                border-radius: 6px;
            }
            QPushButton#closeBtn {
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
            QPushButton#closeBtn:hover {
                color: red;
            }
        """)

        # ---- wrapper（外枠） ----
        wrapper = QWidget(self)
        wrapper.setObjectName("wrapper")
        wrapper_layout = QHBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(4, 4, 4, 4)
        wrapper_layout.setSpacing(0)

        # ---- 本文 ----
        text = QLabel("ドラッグで移動できます。右の × で閉じます。")
        text.setWordWrap(True)
        wrapper_layout.addWidget(text)

        # ---- 閉じるボタン ----
        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(16, 16)
        self.close_btn.clicked.connect(self.close)
        wrapper_layout.addWidget(self.close_btn)

        # ---- BalloonPopup のレイアウト ----
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(wrapper)

        self.resize(100, 16)

    # ---- ドラッグ移動処理 ----
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    # ---- 表示位置指定（ボタンの下など）----
    def show_at(self, widget):
        pos = widget.mapToGlobal(QPoint(0, widget.height()))
        self.move(pos)
        self.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.btn = QPushButton("吹き出しを表示")
        layout.addWidget(self.btn)

        self.popup = BalloonPopup(self)
        self.btn.clicked.connect(self.show_popup)

    def show_popup(self):
        self.popup.show_at(self.btn)


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()
