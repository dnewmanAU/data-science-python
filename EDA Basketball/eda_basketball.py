import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Web scraping
@st.cache  # streamlit will cache the loaded data
def get_stats(year):
    url = (
        "https://www.basketball-reference.com/leagues/NBA_"
        + str(year)
        + "_per_game.html"
    )
    html = pd.read_html(url, header=0)  # omit header data
    df = html[0]
    raw = df.drop(df[df.Age == "Age"].index).fillna(0)
    data = raw.drop(["Rk"], axis=1)  # omit Rk column
    return data


st.title("NBA Player Stats Exploratory Data Analysis")
st.markdown(
    """
Webscraping of NBA player statistics data.
* **Python libraries:** base64, pandas, streamlit, matplotlib, seaborn, numpy
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
"""
)

# Sidebar
st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Year", list(reversed(range(1950, 2022))))
player_stats = get_stats(selected_year)
sorted_unique_team = sorted(player_stats.Tm.unique())  # sorted by unique Team values
selected_team = st.sidebar.multiselect("Team", sorted_unique_team, sorted_unique_team)
unique_pos = ["C", "PF", "SF", "PG", "SG"]
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

# Filter the data based on sidebar specifications (team and position)
df_selected_team = player_stats[
    (player_stats.Tm.isin(selected_team)) & (player_stats.Pos.isin(selected_pos))
]

# Display the data
st.header("Display Player Stats of Selected Team(s)")
st.write(
    "Data Dimensions: "
    + str(df_selected_team.shape[0])
    + " rows and "
    + str(df_selected_team.shape[1])
    + " columns."
)
st.dataframe(df_selected_team)

# Return data as csv downloadable link
def data_to_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv">Download CSV File</a>'
    return href

# Allow user to download the data
st.markdown(data_to_csv(df_selected_team), unsafe_allow_html=True)

# Display heatmap
if st.button("Intercorrelation Headmap"):
    st.header("Intercorrelation Matrix Heatmap")
    df_selected_team.to_csv("output.csv", index=False)
    df = pd.read_csv("output.csv")

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(fig)
