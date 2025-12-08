from PySide6.QtCore import QThread
from windows_capture import WindowsCapture, Frame, InternalCaptureControl
import time
import numpy as np

class CaptureThread(QThread):
    def __init__(self, window_name, process_frame):
        super().__init__()
        self.frame_count = 0
        self.last_time = time.time()

        self.capture = WindowsCapture(
            cursor_capture=False,
            draw_border=False,
            monitor_index=None,
            window_name=window_name,
        )

        @self.capture.event
        def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
            self.frame_count += 1
            current_time = time.time()
            if current_time - self.last_time >= 1:
                fps = self.frame_count / (current_time - self.last_time)
                print(f"FPS: {fps:.2f}")
                self.frame_count = 0
                self.last_time = current_time

            process_frame(np.array(frame.frame_buffer))

        @self.capture.event
        def on_closed():
            print("Capture Session Closed")

    def run(self):
        print(f"Starting Capture: {self.capture}")
        self.running = True
        # Note: start() blocks the main thread, so use start_free_threaded()
        self.capture_control = self.capture.start_free_threaded()
    
    def stop(self):
        print(f"Stopping Capture: {self.capture}")
        self.capture_control.stop()
