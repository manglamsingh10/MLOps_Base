import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import optuna
import pickle

# Load the Iris dataset
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df.drop('target', axis=1), df['target'], test_size=0.2, random_state=42)

def objective(trial):
    # Define the hyperparameter space
    n_estimators = trial.suggest_int('n_estimators', 10, 1000)
    max_depth = trial.suggest_int('max_depth', 1, 10)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 10)
    min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 10)

    # Train a Random Forest Classifier with the current hyperparameters
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
    clf.fit(X_train, y_train)

    # Evaluate the model on the validation set
    accuracy = clf.score(X_test, y_test)

    return -accuracy  # Optuna minimizes the objective function, so we use -accuracy as the objective

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=50)

best_trial = study.best_trial
print(f'Best hyperparameters: {best_trial.params}')
print(f'Best accuracy: {-best_trial.value}')

# Train a new model with the best hyperparameters and save it to a file
best_clf = RandomForestClassifier(n_estimators=best_trial.params['n_estimators'], max_depth=best_trial.params['max_depth'], min_samples_split=best_trial.params['min_samples_split'], min_samples_leaf=best_trial.params['min_samples_leaf'])
best_clf.fit(df.drop('target', axis=1), df['target'])
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best_clf, f)

