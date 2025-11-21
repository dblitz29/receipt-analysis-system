import pytesseract
from PIL import Image


image_path = "receipt1.jpg"
img = Image.open(image_path)

text = pytesseract.image_to_string(img, lang="eng")
print("=== TEXT (Tesseract) ===")
print(text)
