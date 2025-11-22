import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from database.db import SessionLocal
from database.models import Receipt, ReceiptItem
from ocr.ocr_expense import analyze_expense
from ocr.receipt_parser import parse_expense

app = Flask(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def clean_price(val):
    if val is None:
        return None
    s = str(val).strip()
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("receipt")
    if not f:
        return jsonify({"error": "no file"}), 400

    name = secure_filename(f.filename or "receipt.jpg")
    path = os.path.join(UPLOAD_DIR, name)
    f.save(path)

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

        items_out = []
        for item in parsed["items"]:
            price_val = clean_price(item["price_raw"])
            it = ReceiptItem(
                receipt_id=r.id,
                item_name=item["item_name"],
                price=price_val,
            )
            db.add(it)
            items_out.append(
                {
                    "item_name": it.item_name,
                    "price": float(price_val) if price_val is not None else None,
                }
            )

        db.commit()

        return jsonify(
            {
                "receipt_id": r.id,
                "store_name": r.store_name,
                "purchase_datetime": r.purchase_datetime.isoformat() if r.purchase_datetime else None,
                "items": items_out,
                "total_amount_raw": parsed["total_amount_raw"],
            }
        )
    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
