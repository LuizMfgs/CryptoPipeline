import sqlite3
import pandas as pd 


conn = sqlite3.connect(
    "data/crypto.db"
)

query = """
Select
    market_cap_rank,
    name,
    symbol,
    current_price,
    market_cap,
    volatility,
    roi_times
FROM cryptocurrencies
ORDER BY market_cap_rank
LIMIT 20
"""

df = pd.read_sql_query(query,conn)

print(df)

conn.close()    