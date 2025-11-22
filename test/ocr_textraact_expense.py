import os
from dotenv import load_dotenv
import boto3

load_dotenv()

_region = os.getenv("AWS_DEFAULT_REGION")
_textract = boto3.client("textract", region_name=_region)

def analyze_expense(path: str) -> dict:
    with open(path, "rb") as f:
        img = f.read()

    res = _textract.analyze_expense(
        Document={"Bytes": img}
    )

    docs = res.get("ExpenseDocuments", [])
    if not docs:
        return {
            "summary": {},
            "items": [],
        }

    doc = docs[0]

    summary = {}
    for field in doc.get("SummaryFields", []):
        t = field.get("Type", {}).get("Text", "")
        v = field.get("ValueDetection", {}).get("Text", "")
        if t and v:
            summary[t] = v

    items = []
    for group in doc.get("LineItemGroups", []):
        for line_item in group.get("LineItems", []):
            data = {}
            for field in line_item.get("LineItemExpenseFields", []):
                k = field.get("Type", {}).get("Text", "")
                v = field.get("ValueDetection", {}).get("Text", "")
                if k and v:
                    data[k] = v
            if data:
                items.append(data)

    return {
        "summary": summary,
        "items": items,
    }
