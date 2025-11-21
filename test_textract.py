import os
from dotenv import load_dotenv
import boto3

load_dotenv()

region = os.getenv("AWS_DEFAULT_REGION")
textract = boto3.client("textract", region_name=region)

with open("test/receipt1.jpg", "rb") as f:
    img = f.read()

res = textract.analyze_document(
    Document={"Bytes": img},
    FeatureTypes=["TABLES", "FORMS"]
)

lines = []
for b in res.get("Blocks", []):
    if b.get("BlockType") == "LINE":
        t = b.get("Text")
        if t:
            lines.append(t)

for l in lines:
    print(l)
