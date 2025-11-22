from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.db import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True)
    purchase_datetime = Column(DateTime)
    store_name = Column(String(255))

    subtotal = Column(Numeric(18, 2), nullable=True)
    tax = Column(Numeric(18, 2), nullable=True)
    total = Column(Numeric(18, 2), nullable=True)

    raw_ocr_json = Column(Text, nullable=True)

    items = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")


class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))

    item_name = Column(String(255))
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Numeric(18, 2), nullable=True)

    raw_line = Column(Text, nullable=True)

    receipt = relationship("Receipt", back_populates="items")
