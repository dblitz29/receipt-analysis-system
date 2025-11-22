from database.db import SessionLocal
from database.models import Receipt

db = SessionLocal()

rows = db.query(Receipt).all()
for r in rows:
    print(r.id, r.store_name, r.purchase_datetime)

db.close()
