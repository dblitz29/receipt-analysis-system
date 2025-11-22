import os, re, json, boto3
from dotenv import load_dotenv
from botocore.config import Config
from schema_text import SCHEMA

load_dotenv()

REGION   = os.getenv("AWS_DEFAULT_REGION", "ap-southeast-3").strip()
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-pro-v1:0").strip()

brt = boto3.client(
    "bedrock-runtime",
    region_name=REGION,
    config=Config(connect_timeout=60, read_timeout=3600)
)

SYS = (
    "You generate ONE SQLite SELECT query.\n"
    "Output only SQL. No markdown.\n"
    "Use only columns from schema.\n"
    "Never write INSERT/UPDATE/DELETE/DROP/ALTER/CREATE/PRAGMA.\n"
    "If date filter is needed, use DATE(receipts.purchase_datetime)."
)

def _call(prompt: str):
    body = {
        "system": [{"text": SYS}],
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"maxTokens": 256, "temperature": 0.0}
    }

    res = brt.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )
    data = json.loads(res["body"].read())
    return data["output"]["message"]["content"][0]["text"].strip()

def _clean(s: str):
    s = re.sub(r"```(?:sql)?", "", s, flags=re.I).replace("```", "").strip()
    m = re.search(r"(select\b.*)", s, flags=re.I | re.S)
    if m:
        s = m.group(1).strip()
    s = re.sub(r"\s+", " ", s).strip()
    return s if s.endswith(";") else s + ";"

def generate_sql(question: str, schema: str = SCHEMA):
    prompt = f"""
        Schema:
        {schema}

        Question:
        {question}

        Return only SQLite SELECT SQL.
    """.strip()

    return _clean(_call(prompt))

def regenerate_sql(question: str, bad_sql: str, error_msg: str, schema: str = SCHEMA):
    prompt = f"""
        Schema:
        {schema}

        Bad SQL:
        {bad_sql}

        Error:
        {error_msg}

        Fix it. Return only SQLite SELECT SQL.
        Question:
        {question}
    """.strip()

    return _clean(_call(prompt))


if __name__ == "__main__":
    print("model:", MODEL_ID, "| region:", REGION)
    print(generate_sql("Did I buy cocktail?"))
