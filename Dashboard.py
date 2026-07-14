import sqlite3
import pandas as pd 
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide"
)

st.title("Cryptocurrency Market Dashboard")

conn = sqlite3.connect("data/crypto.db")

query = """
    SELECT *
    FROM cryptocurrencies
    WHERE etl_timestamp = (
        SELECT MAX(etl_timestamp)
        FROM cryptocurrencies)
    ORDER BY market_cap_rank
    """
df = pd.read_sql_query(query,conn)

conn.close()

st.subheader("Market Overview")

col1,col2,col3,col4 = st.columns(4)

with col1: 
    st.metric("Tracked Coins",
              len(df))
with col2:
    st.metric("Total Market Cap",
             f"${df['market_cap'].sum():,.0f}")
with col3:
    st.metric(
        "Average Volatility",
        f"${df['volatility'].mean():.2f}%"   
    )
with col4:
    st.metric(
        "Highest Price",
        f"${df['current_price'].max():,.2f}"

    )   
#Stats Table

st.subheader(
    "Top 20 Cryptocurrencies"
)

# Att
last_update = pd.to_datetime(
    df["etl_timestamp"].max()
)

st.caption(
    f"Last Update: {last_update.strftime('%d/%m/%Y %H:%M:%S')}"
)

# Big values formatation
def format_market_value(value):

    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"

    elif value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"

    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    else:
        return f"${value:,.0f}"


# Copy to exibition
df_display = df.head(20).copy()

# Keep important columns
df_display = df_display[
    [
       "name",
        "market_cap_rank",
        "current_price",
        "market_cap",
        "total_volume",
        "price_change_percentage_24h",
        "ath_change_percentage",
        "liquidity_ratio"
    ]
]

# Rename columns
df_display = df_display.rename(
    columns={
        "name": "Cryptocurrency",
        "market_cap_rank": "Rank",
        "current_price": "Current Price",
        "market_cap": "Market Cap",
        "total_volume": "24h Volume",
        "price_change_percentage_24h": "24h Change (%)",
        "ath_change_percentage": "ATH Change (%)",
        "liquidity_ratio": "Liquidity Ratio (%)"
    }
)

df_display["Current Price"] = (
    df_display["Current Price"]
    .apply(lambda x: f"${x:,.2f}")
)

df_display["Market Cap"] = (
    df_display["Market Cap"]
    .apply(format_market_value)
)

df_display["24h Volume"] = (
    df_display["24h Volume"]
    .apply(format_market_value)
)

df_display["24h Change (%)"] = (
    df_display["24h Change (%)"]
    .round(2)
)

df_display["24h Change (%)"] = (
    df_display["24h Change (%)"]
    .round(2)
)

df_display["ATH Change (%)"] = (
    df_display["ATH Change (%)"]
    .round(2)
)

df_display["Liquidity Ratio (%)"] = (
    df_display["Liquidity Ratio (%)"]
    .round(2)
)

# Exibe tabela
st.dataframe(
    df_display,
    hide_index=True,
    use_container_width=True
)

# Volatility Chart

st.subheader(
    "Most Volatile Cryptocurrencies"
)

top_liquidity = (
    df.sort_values(
        "liquidity_ratio",
        ascending=False
    ).head(10)
)

fig = px.bar(
    top_liquidity,
    x="name",
    y="liquidity_ratio",
    title="Top 10 Cryptocurrencies by Liquidity Ratio",
    labels={
        "name": "Cryptocurrency",
        "liquidity_ratio": "Liquidity Ratio (%)"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)