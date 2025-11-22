from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.exc import SQLAlchemyError

from database.db import SessionLocal
from query_engine.text_to_sql import generate_sql, regenerate_sql
from query_engine.safe_sqlite import is_safe_select, run_sql
from query_engine.answer_formatter import format_answer


def ask_db(question: str):
    sql = generate_sql(question)
    print("SQL:", sql)

    if not is_safe_select(sql):
        return "Query blocked."

    db = SessionLocal()
    try:
        try:
            rows = run_sql(db, sql)
        except SQLAlchemyError as e:
            err = str(e.__cause__ or e)

            sql2 = regenerate_sql(question, sql, err)
            print("SQL retry:", sql2)

            if not is_safe_select(sql2):
                return "Query blocked."

            rows = run_sql(db, sql2)
    finally:
        db.close()

    return format_answer(question, rows)


if __name__ == "__main__":
    print("Ask anything about your receipts. Type 'exit' to quit.\n")
    while True:
        q = input("You: ").strip()
        if q.lower() in ["exit", "quit"]:
            break
        print("Bot:", ask_db(q))
