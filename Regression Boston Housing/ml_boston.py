import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor


def user_input_parameters():
    """
    Collect user input parameters from the sidebar.

    Returns
    -------
    DataFrame
        A dataframe containing the selected user input parameters.

    """
    CRIM = st.sidebar.slider("CRIM", x.CRIM.min(), x.CRIM.max(), float(x.CRIM.mean()))
    ZN = st.sidebar.slider("ZN", x.ZN.min(), x.ZN.max(), float(x.ZN.mean()))
    INDUS = st.sidebar.slider(
        "INDUS", x.INDUS.min(), x.INDUS.max(), float(x.INDUS.mean())
    )
    CHAS = st.sidebar.slider("CHAS", x.CHAS.min(), x.CHAS.max(), float(x.CHAS.mean()))
    NOX = st.sidebar.slider("NOX", x.NOX.min(), x.NOX.max(), float(x.NOX.mean()))
    RM = st.sidebar.slider("RM", x.RM.min(), x.RM.max(), float(x.RM.mean()))
    AGE = st.sidebar.slider("AGE", x.AGE.min(), x.AGE.max(), float(x.AGE.mean()))
    DIS = st.sidebar.slider("DIS", x.DIS.min(), x.DIS.max(), float(x.DIS.mean()))
    RAD = st.sidebar.slider("RAD", x.RAD.min(), x.RAD.max(), float(x.RAD.mean()))
    TAX = st.sidebar.slider("TAX", x.TAX.min(), x.TAX.max(), float(x.TAX.mean()))
    PTRATIO = st.sidebar.slider(
        "PTRATIO", x.PTRATIO.min(), x.PTRATIO.max(), float(x.PTRATIO.mean())
    )
    B = st.sidebar.slider("B", x.B.min(), x.B.max(), float(x.B.mean()))
    LSTAT = st.sidebar.slider(
        "LSTAT", x.LSTAT.min(), x.LSTAT.max(), float(x.LSTAT.mean())
    )
    input_params = {
        "CRIM": CRIM,
        "ZN": ZN,
        "INDUS": INDUS,
        "CHAS": CHAS,
        "NOX": NOX,
        "RM": RM,
        "AGE": AGE,
        "DIS": DIS,
        "RAD": RAD,
        "TAX": TAX,
        "PTRATIO": PTRATIO,
        "B": B,
        "LSTAT": LSTAT,
    }
    variables = pd.DataFrame(input_params, index=[0])
    return variables


# Load the Boston House Price dataset
boston = datasets.load_boston()
# Assign the independent variables
x = pd.DataFrame(boston.data, columns=boston.feature_names)
# Assign the dependent variable
y = pd.DataFrame(boston.target, columns=["MEDV"])

# Build the regression model from the boston dataset
boston_model = RandomForestRegressor().fit(x, y)

# App title
st.write(
    """
    # Boston House Price Prediction

    Predict the **Boston House Price**.

    * **Python libraries:** streamlit, pandas, shap, matplotlib, sklearn
    """
)

# Sidebar title
st.sidebar.header("Specify Input Parameters")

# Allow user to input parameters and assign to a data frame
df = user_input_parameters()

# Display selected user input parameters
st.header("Selected Input Parameters")
st.write(df)
st.write("---")  # line break for formatting

# Display the prediction
st.header("Prediction of MEDV")
st.write(boston_model.predict(df))
st.write("---")

# Explaining the model's prediction using SHAP values
explainer = shap.TreeExplainer(boston_model)
shap_values = explainer.shap_values(x)

# Display the plots
st.header("Independent Variable Importance")
fig, ax = plt.subplots()
ax.set_title("Variable importance based on SHAP values (bar)")
shap.summary_plot(shap_values, x, plot_type="bar")
st.pyplot(fig, bbox_inches="tight")
st.write("---")
fig, ax = plt.subplots()
ax.set_title("Variable importance based on SHAP Values")
shap.summary_plot(shap_values, x)
st.pyplot(fig, bbox_inches="tight")
