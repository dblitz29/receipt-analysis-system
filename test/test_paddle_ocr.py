from paddleocr import PaddleOCR
import pprint

ocr = PaddleOCR(lang='en', use_angle_cls=True)

result = ocr.predict("receipt2.jpg")

print("=== TEXT ONLY ===")
for line in result[0]:
    print(line[1][0])
