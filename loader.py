# this file is to load data from the file "colors.csv" into the database, 
# using the credentials from the file "database.json"

import pandas as pd
import psycopg2
import time
import json

data = pd.read_csv(r'colors.csv')
df = pd.DataFrame(data)
# print(df.head)

with open("database.json", "r") as f:
    db = json.load(f)

conn = psycopg2.connect(database = db["database"], user = db["user"], password = db["password"], host = "127.0.0.1", port = "5432")

print("Connected to databse successfully")

cur = conn.cursor()
start = time.time()
cur.execute(
    """
    CREATE TABLE COLORS (
        NAME VARCHAR(30) PRIMARY KEY,
        HEX VARCHAR(10),
        RGB VARCHAR(20)
);
"""
)
for row in df.itertuples():
    cur.execute(f"""
    INSERT INTO COLORS (NAME, HEX, RGB)
    VALUES('{row.Name}','{row.HEX}','{row.RGB}');""")

conn.commit()
cur.close()

end = time.time()
print(f"Wrote the database")
print(f"Time Taken: {end - start} seconds")

conn.close()
