from datetime import datetime
import re

def _to_num(s):
    if not s:
        return None
    s = s.replace(",", "")
    m = re.findall(r"[\d.]+", s)
    return float(m[0]) if m else None

def parse_expense(data: dict) -> dict:
    summary = data.get("summary", {})
    raw_items = data.get("items", [])

    store_name = summary.get("VENDOR_NAME") or summary.get("NAME") or ""

    date_raw = summary.get("INVOICE_RECEIPT_DATE") or summary.get("TRANSACTION_DATE")
    dt = None
    if date_raw:
        for fmt in ("%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                dt = datetime.strptime(date_raw, fmt)
                break
            except ValueError:
                pass

    items = []
    for it in raw_items:
        name = it.get("ITEM") or it.get("DESCRIPTION") or it.get("EXPENSE_ROW") or ""
        qty  = it.get("QUANTITY")
        price = it.get("PRICE") or it.get("UNIT_PRICE")

        items.append({
            "name": name.strip(),
            "qty": int(qty) if qty and str(qty).isdigit() else None,
            "price": _to_num(price),
            "raw_line": it.get("EXPENSE_ROW") or None
        })

    return {
        "store_name": store_name,
        "purchase_datetime": dt,
        "subtotal": _to_num(summary.get("SUBTOTAL")),
        "tax": _to_num(summary.get("TAX")),
        "total": _to_num(summary.get("TOTAL") or summary.get("AMOUNT_DUE")),
        "items": items,
        "raw_json": data,   # biar app.py bisa simpan raw
    }

def parse_receipt(data: dict):
    return parse_expense(data)
