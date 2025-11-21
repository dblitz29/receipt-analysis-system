import easyocr

def main():
    reader = easyocr.Reader(['en'])

    image_path = "receipt1.jpg"
    print("[INFO] Running EasyOCR on:", image_path)

    results = reader.readtext(image_path)

    print("\n=== TEXT ONLY (EasyOCR) ===")
    if not results:
        print("No text detected.")
        return

    for bbox, text, score in results:
        print(f"{score:.2f} - {text}")

if __name__ == "__main__":
    main()
