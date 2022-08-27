import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

st.write(
    """
    # Palmer Penguin Species Prediction

    Predicts the **Palmer Penguin** species using the random forest classifer.

    Data obtained from the [palmerpenguins library](https://github.com/allisonhorst/palmerpenguins) in R by Allison Horst.
    """
)

st.sidebar.header("Penguin Input parameters")

st.sidebar.markdown(
    """
    [CSV input parameters]("penguins_example.csv")
    """
)

uploaded_csv_params = st.sidebar.file_uploader(
    "Upload your input parameters CSV", type=["csv"]
)
if uploaded_csv_params is not None:
    input_df = pd.read_csv(uploaded_csv_params)
else:

    def user_input_params():
        island = st.sidebar.selectbox("Island", ("Biscoe", "Dream", "Torgersen"))
        sex = st.sidebar.selectbox("Sex", ("male", "female"))
        bill_length_mm = st.sidebar.slider("Bill legnth (mm)", 32.1, 59.6, 43.9)
        bill_depth_mm = st.sidebar.slider("Bill depth (mm)", 13.1, 21.5, 17.2)
        flipper_length_mm = st.sidebar.slider(
            "Flipper length (mm)", 172.0, 231.0, 201.0
        )
        body_mass_g = st.sidebar.slider("Body mass (g)", 2700.0, 6300.0, 4207.0)
        input_data = {
            "island": island,
            "sex": sex,
            "bill_depth_mm": bill_depth_mm,
            "bill_length_mm": bill_length_mm,
            "flipper_length_mm": flipper_length_mm,
            "body_mass_g": body_mass_g,
        }
        penguin_params = pd.DataFrame(input_data, index=[0])
        return penguin_params

    input_df = user_input_params()
