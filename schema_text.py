SCHEMA = """
Tables:

receipts:
- id (integer, primary key)
- purchase_datetime (datetime)
- store_name (text)
- subtotal (numeric, nullable)
- tax (numeric, nullable)
- total (numeric, nullable)
- raw_ocr_json (text, nullable)

receipt_items:
- id (integer, primary key)
- receipt_id (integer, foreign key to receipts.id)
- item_name (text)
- quantity (integer, nullable)
- unit_price (numeric, nullable)
- raw_line (text, nullable)

Relationship:
receipt_items.receipt_id -> receipts.id
"""