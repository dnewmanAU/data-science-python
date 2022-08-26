import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

# Get user input parameters for iris flower prediction
# Return dict with key: value params
def iris_input_params():
    sepal_length = st.sidebar.slider("Sepal length", 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider("Sepal width", 2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider("Petal length", 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider("Petal width", 0.1, 2.5, 0.2)
    input_data = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }
    iris_params = pd.DataFrame(input_data, index=[0])
    return iris_params


df = iris_input_params()

# Load the iris dataset from sklearn package
iris_dataset = datasets.load_iris()
x = iris_dataset.data
y = iris_dataset.target

# Classifier using a training model from the iris dataset
clf = RandomForestClassifier()
clf.fit(x, y)

# Make the prediction and its probability from the classifier and input data
prediction = clf.predict(df)
prediction_proba = clf.predict_proba(df)

# App title
st.write(
    """
    # Iris Flower Prediction

    Predict iris flower type based on user input parameters.
    * **Python libraries:** streamlit, pandas, sklearn
    """
)

# Sidebar title
st.sidebar.header("Iris Input Parameters")

# Iris user input parameters
st.subheader("Iris Input Parameters")
st.write(df)

# Iris flower types
st.subheader("Class labels and their corresponding index number")
st.write(iris_dataset.target_names)

# Predicted iris flower based on input parameters
st.subheader("Prediction")
st.write(iris_dataset.target_names[prediction])

# Probability of a predication (index numbers correspond to class labels)
st.subheader("Prediction Probability")
st.write(prediction_proba)
