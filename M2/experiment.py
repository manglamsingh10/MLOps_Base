import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

iris = load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
# params = {'C': 1.0, 'penalty': 'l2'}
# params = {'C': 0.1, 'penalty': 'l1'}
params = {'C': 10.0, 'penalty': 'l2'}

mlflow.set_experiment('Iris Classification')
with mlflow.start_run():
    # Log the model parameters
    mlflow.log_params(params)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Log the metrics
    mlflow.log_metric('accuracy', accuracy)
    
    # Log the model
    mlflow.sklearn.log_model(model,'model')