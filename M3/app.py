from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Load the saved model
model_path = os.path.join(os.path.dirname(__file__), 'best_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return jsonify({'prediction': prediction.tolist()})

@app.route('/', methods=['GET'])
def home():
    return "Model prediction service is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)