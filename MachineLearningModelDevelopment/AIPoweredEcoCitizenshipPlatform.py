import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import joblib

# ------------------------------
# Step 1: Data Ingestion
# ------------------------------

def load_dataset(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded dataset from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

# File paths for three datasets
co2_footprint_file = r"C:\Users\Nikhil Sukthe\Downloads\co2_footprints.csv"
ghgp_data_file = r"C:\Users\Nikhil Sukthe\Downloads\ghgp_data_by_year_2023.csv"
world_energy_file = r"C:\Users\Nikhil Sukthe\Downloads\WorldEnergyConsumption.csv"

# Load the datasets
co2_df = load_dataset(co2_footprint_file)
ghgp_df = load_dataset(ghgp_data_file)
world_energy_df = load_dataset(world_energy_file)

# ------------------------------
# Step 2: Data Cleaning
# ------------------------------
def clean_co2_data(df):
    df['YYYYMM'] = pd.to_datetime(df['YYYYMM'], format='%Y%m')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df.dropna(inplace=True)
    return df

def clean_ghgp_data(df):
    df = df[['Facility Name', 'City', 'State', '2023 Total reported direct emissions']].dropna()
    df['2023 Total reported direct emissions'] = pd.to_numeric(df['2023 Total reported direct emissions'], errors='coerce')
    return df

def clean_world_energy_data(df):
    df['year'] = pd.to_datetime(df['year'], errors='coerce')
    df.dropna(inplace=True)
    return df

# Clean all datasets
co2_df = clean_co2_data(co2_df)
ghgp_df = clean_ghgp_data(ghgp_df)
world_energy_df = clean_world_energy_data(world_energy_df)

# ------------------------------
# Step 3: LSTM Model for Time-Series Forecasting
# ------------------------------
def prepare_lstm_data(df, time_steps=10):
    emissions_data = df.set_index('YYYYMM')['Value'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(emissions_data)

    def create_sequences(data, time_steps):
        x, y = [], []
        for i in range(len(data) - time_steps - 1):
            x.append(data[i:(i + time_steps), 0])
            y.append(data[i + time_steps, 0])
        return np.array(x), np.array(y)

    x, y = create_sequences(scaled_data, time_steps)
    x = x.reshape((x.shape[0], x.shape[1], 1))  # Reshape for LSTM
    return x, y, scaler

# Prepare data for LSTM
x_train, y_train, scaler = prepare_lstm_data(co2_df)

# Build the LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Train the LSTM model
model = build_lstm_model((x_train.shape[1], 1))
model.fit(x_train, y_train, epochs=50, batch_size=32)

# Save the model
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("Model saved as 'model.pkl'")

# ------------------------------
# Step 4: Forecasting
# ------------------------------
def forecast_emissions(model, scaler, data, time_steps=10):
    # Use last time_steps data points for forecasting
    data_scaled = scaler.transform(data.reshape(-1, 1))
    x_input = data_scaled[-time_steps:].reshape((1, time_steps, 1))
    
    predicted_scaled = model.predict(x_input)
    predicted_value = scaler.inverse_transform(predicted_scaled)
    return predicted_value

# Forecast emissions for next month
last_10_values = co2_df['Value'].values[-10:]
predicted_emission = forecast_emissions(model, scaler, last_10_values)
print(f"Predicted CO2 emissions for next month: {predicted_emission[0][0]:.2f} Million Metric Tons")

# ------------------------------
# Step 5: Recommendations
# ------------------------------
def recommend_action(emission_value):
    if emission_value > 100:
        return "High emissions detected! Consider switching to renewable energy."
    elif emission_value > 50:
        return "Moderate emissions. Try to reduce your energy consumption."
    else:
        return "Great job! Your emissions are under control."

# Provide recommendation based on forecasted emissions
recommendation = recommend_action(predicted_emission[0][0])
print(f"Recommendation: {recommendation}")

# ------------------------------
# Step 6: Visualization
# ------------------------------
def plot_emissions(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['YYYYMM'], df['Value'], label='CO2 Emissions')
    plt.title('CO2 Emissions Over Time')
    plt.xlabel('Year')
    plt.ylabel('CO2 Emissions (Million Metric Tons)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the CO2 emissions
plot_emissions(co2_df)
