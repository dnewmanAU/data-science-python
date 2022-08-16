import yfinance as yf
import streamlit as st

# Markdown
st.write(
    """
# Stock Price App

#### Google stock closing price and volume of shares

"""
)

# Get stock data of Google
tickerSymbol = "GOOGL"
tickerData = yf.Ticker(tickerSymbol)

# Data point for each day since inception
tickerDf = tickerData.history(period="1d", start="2004-1-1", end="2022-8-15")

# Plot the closing price and volume of shares
st.write(
    """
### Closing Price
"""
)
st.line_chart(tickerDf.Close)
st.write(
    """
### Volume of Shares
"""
)
st.line_chart(tickerDf.Volume)
