from ..text_recognition import TextRecognizer
import time
import cv2

if __name__ == "__main__":
    ocr = TextRecognizer()
    
    # load image.png as ndarray (BGR) for PaddleOCR
    image = cv2.imread("./image.png", cv2.IMREAD_COLOR)

    start_time = time.time()
    lines = ocr.recognize_text(image)
    end_time = time.time()
    
    for line in lines:
        print("New Line:")
        for textbox in line:
            print(f"Text: {textbox.text}, Box: ({textbox.x}, {textbox.y}, {textbox.w}, {textbox.h})")

    print(f"OCR Time: {(end_time - start_time)*1000:.2f} ms")
