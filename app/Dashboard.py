from app.database.Database import engine
import pandas as pd
import streamlit as st
import plotly.express as px
from app.database.Repository import CryptoRepository
# PAGE CONFIG

rows = CryptoRepository.get_latest_snapshot(

)
st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide"
)

st.title("📈 Cryptocurrency Market Dashboard")
st.markdown("""
Interactive dashboard powered by an ETL pipeline using the CoinGecko API.
""")
st.divider()


# DATABASE


df = pd.DataFrame(
    rows,
    columns=[
        "id",
        "coin_id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "market_cap_rank",
        "total_volume",
        "price_change_percentage_24h",
        "ath_change_percentage",
        "liquidity_ratio",
        "etl_timestamp",
    ],
)


# LAST UPDATE

last_update = pd.to_datetime(
    df["etl_timestamp"].max()
)
st.caption(
    f"🕒 Last Update: {last_update.strftime('%d %b %Y - %H:%M:%S')}"
)
# KPI's

st.subheader("Market Overview")

left, col1, col2, col3, col4, right = st.columns([1,2,2,2,2,1])

with col1:
    st.metric(
        "Tracked Coins",
        len(df)
    )

with col2:
    st.metric(
        "Total Market Cap",
        f"${df['market_cap'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Average 24h Change",
        f"{df['price_change_percentage_24h'].mean():.2f}%"
    )

with col4:
    st.metric(
        "Average Liquidity Ratio",
        f"{df['liquidity_ratio'].mean():.2f}%"
    )

st.caption(
    f"Last Update: {last_update.strftime('%d/%m/%Y %H:%M:%S')}"
)

# FORMAT FUNCTIONS

def format_market_value(value):

    if value >= 1_000_000_000_000:
        return f"${value/1_000_000_000_000:.2f}T"

    elif value >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"

    elif value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"

    else:
        return f"${value:,.0f}"


# TOP 20 TABLE

st.subheader("🏆 Top 20 Cryptocurrencies")
df_display = df.head(20).copy()
df_display = df_display[
    [
        "market_cap_rank",
        "name",
        "current_price",
        "market_cap",
        "total_volume",
        "price_change_percentage_24h",
        "ath_change_percentage",
        "liquidity_ratio"
    ]
]

df_display.rename(
    columns={
        "market_cap_rank": "Rank",
        "name": "Cryptocurrency",
        "current_price": "Current Price",
        "market_cap": "Market Cap",
        "total_volume": "24h Volume",
        "price_change_percentage_24h": "24h Change (%)",
        "ath_change_percentage": "Distance from ATH (%)",
        "liquidity_ratio": "Liquidity Ratio (%)"
    },
    inplace=True
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

df_display["Distance from ATH (%)"] = (
    df_display["Distance from ATH (%)"]
    .round(2)
)

df_display["Liquidity Ratio (%)"] = (
    df_display["Liquidity Ratio (%)"]
    .round(2)
)

st.dataframe(
    df_display,
    hide_index=True,
    use_container_width=True
)
st.divider()

st.subheader("📊 Market Analytics")

# CHARTS
top_liquidity = CryptoRepository.get_top_liquidity()

top_change = CryptoRepository.get_top_gainers()

left_space, col_left, col_right, right_space = st.columns([1,4,4,1])

# ---------- Liquidity ----------

fig_liquidity = px.bar(
    top_liquidity,
    x="name",
    y="liquidity_ratio",
    color="liquidity_ratio",
    color_continuous_scale="Turbo",
    title="Top 10 Highest Liquidity Ratio",
    labels={
        "name":"Cryptocurrency",
        "liquidity_ratio":"Liquidity Ratio (%)"
    }
)

fig_liquidity.update_layout(

    title_x=0.5,

    template="plotly_white",

    xaxis_title=None,

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

# ---------- 24h Change ----------

fig_change = px.bar(
    top_change,
    x="name",
    y="price_change_percentage_24h",
    color="price_change_percentage_24h",
    color_continuous_scale="RdYlGn",
    title="Top 10 Largest 24h Gains",
    labels={
        "name":"Cryptocurrency",
        "price_change_percentage_24h":"24h Change (%)"
    }
)

fig_change.update_layout(

    title_x=0.5,

    template="plotly_white",

    xaxis_title=None,

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)
st.divider()

left, col3, col4, right = st.columns([1,4,4,1])

# MARKET CAP CHART

with col3:

    top_marketcap = CryptoRepository.get_top_marketcap()

    fig_marketcap = px.bar(

        top_marketcap,

        x="name",

        y="market_cap",

        color="market_cap",

        color_continuous_scale="Viridis",

        title="Top 10 Market Cap"

    )

    fig_marketcap.update_layout(

        title_x=0.5,

        template="plotly_white",

        xaxis_title=None
    )

    st.plotly_chart(
        fig_marketcap,
        use_container_width=True
    )
    
#TRADING VOLUME
with col4:

    top_volume = CryptoRepository.get_top_volume()

    fig_volume = px.bar(

        top_volume,

        x="name",

        y="total_volume",

        color="total_volume",

        color_continuous_scale="Blues",

        title="Top 10 Trading Volume"

    )

    fig_volume.update_layout(

        title_x=0.5,

        template="plotly_white",

        xaxis_title=None
    )

    st.plotly_chart(

        fig_volume,

        use_container_width=True

    )
    st.divider()

st.caption(
    "Developed with Python • Streamlit • PostgreeSQL • Plotly • CoinGecko API"
)