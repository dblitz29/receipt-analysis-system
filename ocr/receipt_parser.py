from datetime import datetime

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

    return {
        "store_name": store_name,
        "purchase_datetime": dt,
        "subtotal_raw": summary.get("SUBTOTAL"),
        "tax_raw": summary.get("TAX"),
        "total_raw": summary.get("TOTAL") or summary.get("AMOUNT_DUE"),
        "items": raw_items,
        "raw": data,
    }
