import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

# Web scraping of S&P 500 data
@st.cache  # only download the data once
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = pd.read_html(url, header=0)
    df = html[0]
    return df


df = load_data()
sector = df.groupby("GICS Sector")

st.title("S&P 500 Stock Market Index")

st.markdown(
    """
Retrives the **S&P 500 Stock Market Index** from Wikipedia and the corresponding year-to-date **stock closing price**.
* **Python libraries:** streamlit, pandas, base64, matplotlip, yfinance
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
"""
)

st.sidebar.header("Filters")
# Sidebar filters
sorted_sector_unique = sorted(df["GICS Sector"].unique())
selected_sector = st.sidebar.multiselect(
    "Sector(s):", sorted_sector_unique, sorted_sector_unique
)
# Filter data based on sidebar selected sectors
df_selected_sector = df[df["GICS Sector"].isin(selected_sector)]
plot_num = st.sidebar.slider("Number of companies to plot:", 1, 5)

# Display the filtered data
st.header("Companies in Selected Sectors")
st.write(
    "Data dimensions: "
    + str(df_selected_sector.shape[0])
    + " rows and "
    + str(df_selected_sector.shape[1])
    + " columns."
)
st.dataframe(df_selected_sector)

# Return data as csv downloadable link
def data_to_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href


# Allow user to download the data
st.markdown(data_to_csv(df_selected_sector), unsafe_allow_html=True)

# Retrieve the stock closing price of the filtered data using yfinance
if not df_selected_sector.empty:
    plot_data = yf.download(
        tickers=list(df_selected_sector[:10].Symbol),
        period="ytd",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None,
    )

# Plot the stock closing price
def price_plot(symbol):
    df = pd.DataFrame(plot_data[symbol].Close)
    df["Date"] = df.index
    fig, ax = plt.subplots()
    ax.fill_between(df.Date, df.Close, color="skyblue", alpha=0.3)
    ax.plot(df.Date, df.Close, color="skyblue", alpha=0.8)
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    ax.set_title(symbol, fontweight="bold")
    ax.set_xlabel("Date", fontweight="bold")
    ax.set_ylabel("Closing Price", fontweight="bold")
    return st.pyplot(fig)


# Show the plots
st.header("Stock Closing Price")
for i in list(df_selected_sector.Symbol)[:plot_num]:
    price_plot(i)
