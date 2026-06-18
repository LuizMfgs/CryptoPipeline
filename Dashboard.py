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

st.subheader("Top 20 Cryptocurrencies") 
st.dataframe(
    df.head(20)
)
# Market Cap Chart

st.subheader("Top 10 Market Caps")

top10 = (
    df.sort_values(
        "market_cap",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top10,
    x="name",
    y="market_cap",
    title="Top 10 Cryptocurrencies by Market Cap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Volatility Chart

st.subheader(
    "Most Volatile Cryptocurrencies"
)

top_volatility = (
    df.sort_values(
        "volatility",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_volatility,
    x="name",
    y="volatility",
    title="Most Volatile Cryptocurrencies (24h)",
    labels={
        "name": "Cryptocurrency",
        "volatility": "24h Volatility (%)"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)