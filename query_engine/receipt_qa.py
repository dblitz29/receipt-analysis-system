from sqlalchemy.exc import SQLAlchemyError

from database.db import SessionLocal
from .text_to_sql import generate_sql, regenerate_sql
from .safe_sqlite import is_safe_select, run_sql
from .answer_formatter import format_answer


def ask_receipt_db(question: str):
    sql = generate_sql(question)

    if not is_safe_select(sql):
        return {
            "sql": sql,
            "answer": "Query blocked.",
            "rows": []
        }

    db = SessionLocal()
    try:
        try:
            rows = run_sql(db, sql)
        except SQLAlchemyError as e:
            err = str(e.__cause__ or e)

            sql2 = regenerate_sql(question, sql, err)

            if not is_safe_select(sql2):
                return {
                    "sql": sql2,
                    "answer": "Query blocked.",
                    "rows": []
                }

            sql = sql2
            rows = run_sql(db, sql)
    finally:
        db.close()

    answer = format_answer(question, rows)

    return {
        "sql": sql,
        "answer": answer,
        "rows": rows
    }