from datetime import datetime

def parse_expense(data: dict) -> dict:
    summary = data.get("summary", {})
    raw_items = data.get("items", [])

    store_name = summary.get("VENDOR_NAME") or summary.get("RESTAURANT_NAME") or ""

    date_raw = summary.get("INVOICE_RECEIPT_DATE") or summary.get("TRANSACTION_DATE")
    dt = None
    if date_raw:
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                dt = datetime.strptime(date_raw, fmt)
                break
            except ValueError:
                pass

    total_raw = summary.get("TOTAL") or summary.get("AMOUNT_DUE")

    items = []
    for it in raw_items:
        name = it.get("ITEM") or it.get("DESCRIPTION") or ""
        price_raw = it.get("PRICE") or it.get("NET_AMOUNT")
        qty_raw = it.get("QUANTITY")

        items.append(
            {
                "item_name": name,
                "price_raw": price_raw,
                "quantity_raw": qty_raw,
                "raw": it,
            }
        )

    return {
        "store_name": store_name,
        "purchase_datetime": dt,
        "purchase_date_raw": date_raw,
        "total_amount_raw": total_raw,
        "items": items,
    }
