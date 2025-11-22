from database.db import SessionLocal
from database.models import Receipt, ReceiptItem
from ocr.ocr_expense import analyze_expense
from ocr.receipt_parser import parse_expense

def clean_price(val):
    if val is None:
        return None
    s = str(val).strip()
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

def import_one(path: str):
    raw = analyze_expense(path)
    parsed = parse_expense(raw)

    db = SessionLocal()
    try:
        r = Receipt(
            purchase_datetime=parsed["purchase_datetime"],
            store_name=parsed["store_name"],
        )
        db.add(r)
        db.flush()

        for item in parsed["items"]:
            price_val = clean_price(item["price_raw"])
            it = ReceiptItem(
                receipt_id=r.id,
                item_name=item["item_name"],
                price=price_val,
            )
            db.add(it)

        db.commit()
        print("saved receipt", r.id, "from", path)
    finally:
        db.close()

if __name__ == "__main__":
    import_one("test/receipt1.jpg")
