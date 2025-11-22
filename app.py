import os
from flask import Flask, request, jsonify

from database.db import SessionLocal
from ocr.ocr_expense import run_ocr
from ocr.receipt_parser import parse_receipt
from database.models import Receipt, ReceiptItem
import json
from query_engine.receipt_qa import ask_receipt_db
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)
@app.get("/")
def home():
    return render_template("index.html")


@app.get("/receipts-ui")
def receipts_ui():
    return render_template("receipts.html")


@app.post("/upload")
def upload_receipt():
    if "file" not in request.files:
        return {"error": "no file"}, 400

    f = request.files["file"]
    if f.filename == "":
        return {"error": "empty filename"}, 400

    img_bytes = f.read()

    # OCR
    ocr_raw = run_ocr(img_bytes)
    data = parse_receipt(ocr_raw)

    # Save to DB
    db = SessionLocal()
    try:
        r = Receipt(
            store_name=data["store_name"],
            purchase_datetime=data["purchase_datetime"],
            subtotal=data["subtotal"],
            tax=data["tax"],
            total=data["total"],
            raw_ocr_json=json.dumps(data["raw_json"])
        )
        db.add(r)
        db.flush()

        for item in data["items"]:
            db.add(
                ReceiptItem(
                    receipt_id=r.id,
                    item_name=item["name"],
                    quantity=item["qty"],
                    unit_price=item["price"]
                )
            )

        db.commit()
        return {"status": "ok", "receipt_id": r.id}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 500
    finally:
        db.close()

@app.post("/ask")
def ask():
    js = request.get_json()
    q = js.get("question", "").strip()

    if not q:
        return {"error": "question is empty"}, 400

    res = ask_receipt_db(q)
    return res

@app.get("/receipts")
def list_receipts():
    db = SessionLocal()
    rows = db.query(Receipt).all()

    out = []
    for r in rows:
        out.append({
            "id": r.id,
            "store": r.store_name,
            "date": r.purchase_datetime,
            "total": r.total
        })

    db.close()
    return jsonify(out)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)