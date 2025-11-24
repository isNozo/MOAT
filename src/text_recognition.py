from paddleocr import PaddleOCR, TextDetection
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
        self.results = []

        self.ocr = PaddleOCR(
            text_detection_model_name="PP-OCRv5_mobile_det",
            text_recognition_model_name="PP-OCRv5_mobile_rec",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            text_det_limit_side_len=1920,
            )
        self.det = TextDetection(
            model_name="PP-OCRv4_mobile_det",
            limit_side_len=1920,
            )

    def zip_with(func, *iterables):
        return [func(*args) for args in zip(*iterables)]

    def toTextBox(text, box):
        return TextBox(
            text=text,
            x=box[0],
            y=box[1],
            w=box[2] - box[0],
            h=box[3] - box[1]
            )

    def recognize_text(self, frame_buffer):
        try:
            result = self.ocr.predict(frame_buffer, return_word_box=True)

            if not result:
                return None
            else:
                wordss = result[0]["text_word"]
                boxess = result[0]["text_word_boxes"]

                lines = []
                for texts, boxes in zip(wordss, boxess):
                    line = TextRecognizer.zip_with(TextRecognizer.toTextBox, texts, boxes)
                    lines.append(line)

                self.results = lines

                return self.results
        except Exception as e:
            print(f"Failed to process image: {e}")
            return None
