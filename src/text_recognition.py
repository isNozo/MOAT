import os
import glob
import shutil
import cv2
from dataclasses import dataclass

@dataclass
class TextBox:
    text: str
    x: int
    y: int
    w: int
    h: int

class TextRecognizer:
    def __init__(self):
        self.ensure_oneocr_files()
        import oneocr
        self.results = []
        self.ocr = oneocr.OcrEngine()

    def recognize_text(self, image):
        try:
            is_success, eimg = cv2.imencode(".png", image)
            res = self.ocr.recognize_cv2(eimg)
            if not res:
                return None
            else:
                lines = []
                for line in res["lines"]:
                    words = []
                    for word in line["words"]:
                        txt = word["text"]
                        pos = word["bounding_rect"]
                        pos_x_min = min(pos["x1"], pos["x2"], pos["x3"], pos["x4"])
                        pos_x_max = max(pos["x1"], pos["x2"], pos["x3"], pos["x4"])
                        pos_y_min = min(pos["y1"], pos["y2"], pos["y3"], pos["y4"])
                        pos_y_max = max(pos["y1"], pos["y2"], pos["y3"], pos["y4"])
                        words.append(TextBox(
                            text=txt,
                            x=int(pos_x_min),
                            y=int(pos_y_min),
                            w=int(pos_x_max-pos_x_min),
                            h=int(pos_y_max-pos_y_min)
                            ))
                    lines.append(words)
                self.results = lines
                return lines

        except Exception as e:
            print(f"Failed to process image: {e}")
            return None

    def find_snipping_tool_dir(self):
        base_dir = r"C:\Program Files\WindowsApps"
        pattern = os.path.join(base_dir, "Microsoft.ScreenSketch_*")
        for folder in glob.glob(pattern):
            snip_dir = os.path.join(folder, "SnippingTool")
            if os.path.isdir(snip_dir):
                return snip_dir
        return None

    def ensure_oneocr_files(self):
        target_dir = os.path.join(os.path.expanduser('~'), '.config', 'oneocr')
        os.makedirs(target_dir, exist_ok=True)

        src_dir = self.find_snipping_tool_dir()
        if not src_dir:
            print("SnippingTool folder not found.")
            return False

        files = ["oneocr.dll", "oneocr.onemodel", "onnxruntime.dll"]

        copied = False

        for fname in files:
            src = os.path.join(src_dir, fname)
            dst = os.path.join(target_dir, fname)

            if os.path.exists(dst):
                print(f"Exists: {dst}")
                continue

            shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
            copied = True

        return copied