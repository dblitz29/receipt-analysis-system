import os
from dotenv import load_dotenv
import boto3

load_dotenv()

_region = os.getenv("AWS_DEFAULT_REGION")
_tex = boto3.client("textract", region_name=_region)

def analyze_expense(path: str) -> dict:
    with open(path, "rb") as f:
        b = f.read()
    return run_ocr(b)

def run_ocr(img_bytes: bytes):
    res = _tex.analyze_expense(Document={"Bytes": img_bytes})
    docs = res.get("ExpenseDocuments", [])

    if not docs:
        return {"summary": {}, "items": []}

    doc = docs[0]

    summary = {}
    for field in doc.get("SummaryFields", []):
        t = field.get("Type", {}).get("Text")
        v = field.get("ValueDetection", {}).get("Text")
        if t and v:
            summary[t] = v

    items = []
    for group in doc.get("LineItemGroups", []):
        for line_item in group.get("LineItems", []):
            data = {}
            for f in line_item.get("LineItemExpenseFields", []):
                k = f.get("Type", {}).get("Text")
                v = f.get("ValueDetection", {}).get("Text")
                if k and v:
                    data[k] = v
            if data:
                items.append(data)

    return {"summary": summary, "items": items}
