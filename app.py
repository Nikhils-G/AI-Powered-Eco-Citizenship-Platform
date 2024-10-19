from flask import Flask, render_template, request, jsonify, send_from_directory
import pickle
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Ensure the static folder exists
os.makedirs(app.static_folder, exist_ok=True)

# Load the model
model_path = 'model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Assume the input is JSON data with features for prediction
    data = request.json
    features = [data['dashboard'], data['Activities'], data['Community'],data['Rewards'], data['Insights'], data['Challenges']]  # Adjust based on your model's input
    
    # Make a prediction using the model
    prediction = model.predict([features])
    
    # Return the prediction result as a JSON response
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
