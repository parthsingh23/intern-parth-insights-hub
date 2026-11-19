import sqlite3

import pandas as pd

csv_path = "data_pipeline/output/clean_sales.csv"
db_path = "data_pipeline/output/sales.db"

sales = pd.read_csv(csv_path)

conn = sqlite3.connect(db_path)

sales.to_sql(name="sales", con=conn, if_exists="replace", index=False)


conn.close()
