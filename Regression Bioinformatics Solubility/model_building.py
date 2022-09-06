import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

# Read in the data
delaney_with_descriptors_url = "https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv"
dataset = pd.read_csv(delaney_with_descriptors_url)
x = dataset.drop(["logS"], axis=1)
y = dataset.iloc[:, -1]

# Linear Regression Model
model = linear_model.LinearRegression()
model.fit(x, y)

# Model Prediction
y_pred = model.predict(x)

# Model Performance
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)
print("Mean squared error (MSE): %.2f" % mean_squared_error(y, y_pred))
print("Coefficient of determination (R^2): %.2f" % r2_score(y, y_pred))

#   Model Equation
print(
    "LogS = %.2f %.2f LogP %.4f MW + %.4f RB %.2f AP"
    % (model.intercept_, model.coef_[0], model.coef_[1], model.coef_[2], model.coef_[3])
)

# Data Visualistion
plt.figure(figsize=(5, 5))
plt.scatter(x=y, y=y_pred, c="#4DA6FF", alpha=0.3)
# add trendline
z = np.polyfit(y, y_pred, 1)
p = np.poly1d(z)

plt.plot(y, p(y), "#F8766D")
plt.ylabel("Predicted LogS")
plt.xlabel("Experimental LogS")
# plt.show()

pickle.dump(model, open("solubility_model.pkl", "wb"))
