import sqlite3

db_path = "data_pipeline/output/sales.db"
sql_path = "data_pipeline/queries.sql"

conn = sqlite3.connect(db_path)

with open(sql_path, "r") as file:
    sql_content = file.readlines()

statement = []
query_number = 1

for line in sql_content:
    if line.strip().startswith("--"):
        continue

    statement.append(line)

    sql_statement = "".join(statement).strip()

    if sqlite3.complete_statement(sql_statement):
        if sql_statement:
            print(f"\n{'=' * 50}")
            print(f"Query {query_number}")
            print("=" * 50)

            result = conn.execute(sql_statement)

            for row in result.fetchall():
                print(row)

            query_number += 1

        statement = []

conn.close()
