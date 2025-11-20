import sys
import random
import time
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect, QPoint, QObject, Signal, Slot, QThread

# 重い処理（例）
def text_process(text):
    time.sleep(0.5)  # 時間がかかる処理の想定
    return f"[Processed] {text}"


# Worker（別スレッドで実行される）
class TextProcessWorker(QThread):
    finished = Signal(str, int)  # text結果, task_id を返す

    def __init__(self, text, task_id):
        super().__init__()
        self.text = text
        self.task_id = task_id

    def run(self):
        print(f"Worker started for task_id: {self.task_id}")
        result = text_process(self.text)
        self.finished.emit(result, self.task_id)


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
        self.in_any_rect = False

        # 現在のタスクID（スレッド管理用）
        self.current_task_id = 0
        self.thread_queue = []

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        rects = get_rects()

        # マウスがいずれかの矩形内に入っている場合
        for text, rect in rects:
            if rect.contains(pos):
                if not self.in_any_rect:
                    self.in_any_rect = True
                    self.startTextProcess(rect, text)
                return

        # マウスが矩形外に出た場合
        self.in_any_rect = False
        self.popup.hide()

    # 重い処理を別スレッドで開始
    def startTextProcess(self, rect, text):
        # ローディング表示
        self.updatePopup(rect, "Loading...")

        # タスクID を更新（古い結果は無視する）
        self.current_task_id += 1

        # 別スレッドのセットアップ
        thread = TextProcessWorker(text, self.current_task_id)
        thread.finished.connect(self.onWorkerFinished)
        thread.start()
        self.thread_queue.append(thread)  # 参照を保持

        self._pending_rect = rect  # 処理後に同じ位置に表示する

    # スレッド完了時に呼ばれる
    @Slot(str, int)
    def onWorkerFinished(self, result_text, task_id):
        print(f"Worker finished for task_id: {task_id}")

        self.thread_queue.pop(0)  # 参照を解放

        # 古いタスクの結果なら無視する
        if task_id != self.current_task_id:
            return
        
        # マウスが矩形外に出ていたら無視する
        if self.in_any_rect is False:
            return

        # 最新タスクなのでポップアップ更新
        self.updatePopup(self._pending_rect, result_text)

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
