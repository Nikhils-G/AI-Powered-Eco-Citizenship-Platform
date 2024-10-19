from flask import Flask, render_template, request, jsonify, send_from_directory
import pickle
import os
import joblib  # for loading the scaler

app = Flask(__name__, static_folder='static', template_folder='templates')

# Ensure the static folder exists
os.makedirs(app.static_folder, exist_ok=True)

# Load the model
model_path = 'model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Load the scaler
scaler_path = 'scaler.pkl'
with open(scaler_path, 'rb') as f:
    scaler = joblib.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data
    data = request.json
    features = [[
        data['dashboard'],
        data['Activities'],
        data['Community'],
        data['Rewards'],
        data['Insights'],
        data['Challenges']
    ]]  # Make sure to pass features as a 2D array
    
    # Scale the features using the scaler
    scaled_features = scaler.transform(features)

    # Make prediction using the model
    prediction_scaled = model.predict(scaled_features)

    # Inverse transform the prediction back to the original scale
    prediction = scaler.inverse_transform([prediction_scaled])

    # Return the result as JSON
    return jsonify({'prediction': prediction[0][0]})

if __name__ == '__main__':
    app.run(debug=True)
