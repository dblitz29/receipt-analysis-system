from sqlalchemy import text

def is_safe_select(sql: str):
    s = sql.strip().lower()

    if not s.startswith("select"):
        return False

    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "pragma"]
    for f in forbidden:
        if f in s:
            return False

    return True


def run_sql(db, sql: str):
    rows = db.execute(text(sql)).fetchall()

    out = []
    for r in rows:
        if len(r) == 1:
            out.append(r[0])
        else:
            out.append(list(r))
    return out
