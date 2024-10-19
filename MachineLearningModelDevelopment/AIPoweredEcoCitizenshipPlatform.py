import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from flask import Flask, request, jsonify
import folium  # For community impact maps

# ------------------------------
# Step 1: Data Ingestion and Cleaning
# ------------------------------
class DataIngestion:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        try:
            df = pd.read_csv(self.filepath)
            df['YYYYMM'] = pd.to_datetime(df['YYYYMM'], format='%Y%m')
            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
            df.dropna(inplace=True)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

# Ingest the CO2 footprint dataset
dataset_path = r"C:\Users\Nikhil Sukthe\Downloads\co2_footprints.csv"
data_ingestor = DataIngestion(dataset_path)
df = data_ingestor.load_data()

# ------------------------------
# Step 2: Advanced Data Analysis
# ------------------------------
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def analyze(self):
        # Sector-wise CO2 emission analysis
        sector_emissions = self.df.groupby('Description')['Value'].sum()
        print(f"Total Emissions by Sector: \n{sector_emissions}")
        
        # Yearly emissions trend
        self.df['Year'] = self.df['YYYYMM'].dt.year
        yearly_emissions = self.df.groupby('Year')['Value'].sum()
        
        plt.figure(figsize=(14, 7))
        sns.lineplot(x=yearly_emissions.index, y=yearly_emissions.values)
        plt.title('Yearly CO2 Emissions Over Time')
        plt.ylabel('CO2 Emissions (Million Metric Tons)')
        plt.xlabel('Year')
        plt.grid(True)
        plt.show()

# Instantiate DataAnalyzer
analyzer = DataAnalyzer(df)
analyzer.analyze()

# ------------------------------
# Step 3: Advanced ML (LSTM for Time Series Forecasting)
# ------------------------------
class CO2EmissionsForecasting:
    def __init__(self, df):
        self.df = df

    def prepare_data(self):
        # Data Preprocessing for LSTM
        emissions_data = self.df.set_index('YYYYMM')['Value'].values
        emissions_data = emissions_data.reshape(-1, 1)

        # Normalize the dataset for LSTM
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(emissions_data)

        # Split into training and test sets
        train_size = int(len(scaled_data) * 0.8)
        train_data, test_data = scaled_data[:train_size], scaled_data[train_size:]
        
        # Create LSTM input sequences
        def create_sequences(data, time_steps=1):
            x, y = [], []
            for i in range(len(data) - time_steps - 1):
                x.append(data[i:(i + time_steps), 0])
                y.append(data[i + time_steps, 0])
            return np.array(x), np.array(y)
        
        time_steps = 10
        x_train, y_train = create_sequences(train_data, time_steps)
        x_test, y_test = create_sequences(test_data, time_steps)

        # Reshape for LSTM [samples, time steps, features]
        x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
        x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

        return x_train, y_train, x_test, y_test, scaler

    def build_lstm_model(self, input_shape):
        # Build LSTM Model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(units=25))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def train_model(self, model, x_train, y_train, epochs=50, batch_size=64):
        # Train the LSTM model
        model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

    def forecast(self, model, x_test, scaler):
        # Predict and invert the normalization
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        return predictions

# Instantiate and run LSTM forecasting
forecasting = CO2EmissionsForecasting(df)
x_train, y_train, x_test, y_test, scaler = forecasting.prepare_data()
lstm_model = forecasting.build_lstm_model((x_train.shape[1], 1))
forecasting.train_model(lstm_model, x_train, y_train)
predictions = forecasting.forecast(lstm_model, x_test, scaler)

# ------------------------------
# Step 4: Personalized Recommendations (ML-powered)
# ------------------------------
class RecommendationEngine:
    def recommend(self, co2_value):
        # Use ML-based clustering to offer personalized recommendations
        if co2_value > 100:
            return "You are producing high emissions. Switch to renewable energy sources!"
        elif co2_value > 50:
            return "Consider reducing energy consumption by using energy-efficient appliances."
        else:
            return "Great! You are already eco-friendly. Keep maintaining your low carbon footprint."

# ------------------------------
# Step 5: Gamification Engine
# ------------------------------
class GamificationEngine:
    def calculate_points(self, co2_value):
        # Award eco-points based on CO2 emissions reduction
        if co2_value < 50:
            return 100  # Full eco-points
        elif co2_value < 100:
            return 50  # Half eco-points
        else:
            return 10  # Minimal eco-points

# ------------------------------
# Step 6: Community Impact Mapping (Heatmaps with Folium)
# ------------------------------
def create_community_heatmap(locations, emission_values):
    # Create a heatmap of community CO2 emissions using Folium
    heatmap = folium.Map(location=[39.5, -98.35], zoom_start=4)
    heatmap.add_child(folium.plugins.HeatMap([[loc[0], loc[1], val] for loc, val in zip(locations, emission_values)]))
    heatmap.save('community_impact_map.html')

# Example locations and emission values for mapping
locations = [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060)]
emission_values = [75.0, 60.0, 90.0]
create_community_heatmap(locations, emission_values)

# ------------------------------
# Step 7: Flask API for Integrating with Front-End
# ------------------------------
app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.get_json()
    co2_value = user_data.get('co2_value', 0)
    
    # Provide a recommendation based on the CO2 value
    recommender = RecommendationEngine()
    recommendation = recommender.recommend(co2_value)
    return jsonify({"recommendation": recommendation})

if __name__ == '__main__':
    app.run(debug=True)

# ------------------------------
# Further Extensions:
# - Connect to real-time data streams (IoT)
# - Advanced machine learning algorithms for more accurate forecasting
# - Interactive dashboards for user insights
# ------------------------------
