import sqlite3

conn = sqlite3.connect(
    "data/crypto.db"
)

cursor = conn.cursor()

cursor.execute(
    "DROP TABLE IF EXISTS cryptocurrencies"
)

conn.commit()
conn.close()

print("Database reset completed.")