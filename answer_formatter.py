import os, json, boto3
from dotenv import load_dotenv
from botocore.config import Config

load_dotenv()

REGION   = os.getenv("AWS_DEFAULT_REGION", "ap-southeast-2").strip()
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-pro-v1:0").strip()

brt = boto3.client(
    "bedrock-runtime",
    region_name=REGION,
    config=Config(connect_timeout=60, read_timeout=3600)
)

SYS = (
    "You answer questions about food receipts.\n"
    "If rows is empty, say so politely.\n"
    "If rows has data, use ONLY that data.\n"
    "Keep the answer short and natural."
)

def format_answer(question: str, rows):
    has_data = "yes" if rows else "no"

    prompt = f"""
Question:
{question}

has_data: {has_data}
rows:
{rows}

Answer naturally. Don't add new facts.
""".strip()

    body = {
        "system": [{"text": SYS}],
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"maxTokens": 160, "temperature": 0.3}
    }

    res = brt.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )
    data = json.loads(res["body"].read())
    return data["output"]["message"]["content"][0]["text"].strip()
