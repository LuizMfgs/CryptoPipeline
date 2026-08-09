from app.database.Database import engine
import pandas as pd 

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

df = pd.read_sql(
    query,engine
)

print(df)

 