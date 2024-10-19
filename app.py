from flask import Flask, render_template, request, jsonify, send_from_directory
import pickle
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Ensure the static folder exists
os.makedirs(app.static_folder, exist_ok=True)


model_path = 'model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route('/predict', methods=['POST'])
def predict():
    
    data = request.json
    features = [data['dashboard'], data['Activities'], data['Community'],data['Rewards'], data['Insights'], data['Challenges']]  
    
    
    prediction = model.predict([features])
    
    
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
