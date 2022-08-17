import yfinance as yf
import streamlit as st

# Markdown
st.write(
    """
# Stock Price App

#### Stock closing price and volume of shares

"""
)

# Get stock data
tickerData = yf.Ticker("MSFT")

# Data point for each day for 10 years
tickerDf = tickerData.history(period="1d", start="2012-1-1", end="2022-8-15")

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
