import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

# Load iris dataset
iris = load_iris()

# convert array into dataframe 
DF = pd.DataFrame(np.array(iris['data']))
  
DF.to_csv('iris.csv',index=False)
X = iris.data[:, :2]  # we only take the first two features.
y = iris.target


# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# mlflow.create_experiment("my_experiment")

# Create an MLflow experiment
mlflow.set_experiment("my_experiment")

# Define hyperparameters
params = {"C": 1.0, "max_iter": 100}

# Train the model
with mlflow.start_run():
    mlflow.log_params(params)
    logreg = LogisticRegression(**params)
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(logreg, "model")