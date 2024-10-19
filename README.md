
# AI-Powered Eco-Citizenship Platform for Carbon Footprint Reduction

This project is an AI-powered platform that allows individuals and communities to track and reduce their carbon footprint. Leveraging machine learning models, real-time data from public carbon emissions datasets, and user input, the platform provides personalized recommendations, visualizations, and rewards (eco-points) to encourage sustainable living.

## Tech Stack

- AI/ML: Jupyter Notebook, Python (for data preprocessing, model development), Machine Learning model development (LSTM for time-series forecasting)
- Data Sources: Public carbon emissions datasets (CO2 Emissions Data, EPA Greenhouse Gas Reporting Program, World Energy Consumption)
- Frontend: React.js, HTML, CSS (User Interface for tracking eco-points, personal dashboard, and visualizations)
- Backend: Python (Flask for API creation, model serving)
- Database: (Optional) SQLite or PostgreSQL for storing user data, eco-points history, and community footprint metrics

## Project Structure
# Frontend:
## Technology: Built using React.js.
## Purpose: The frontend provides an intuitive user interface where individuals can:
- Input their daily activities (e.g., energy consumption, transportation habits).
- View real-time personal carbon footprint metrics.
- Track eco-points earned through eco-friendly actions.
- Visualize community carbon footprint data through interactive charts and maps.
- Receive personalized recommendations for reducing emissions based on past activities and forecasted trends.

## Backend:
  ##  Technology: Developed in Python using the Flask framework.
- Purpose: The backend processes user activity data and integrates it with external datasets, including public carbon emissions data. It provides:
- Data Processing: Real-time feedback and personalized suggestions for reducing carbon footprints.
- Machine Learning: Forecasting future carbon emissions using time-series models (LSTM).
- API Endpoints: Exposes APIs that the frontend can call for predictions, eco-point calculations, and community metrics.
- Integration: Combines personal user data with large-scale datasets to offer insights and community comparisons.


## Features

- Personal Carbon Footprint Tracking: Users can input their daily activities, such as energy consumption, and track their CO2 emissions.
- Community Engagement: Users can view and compare their footprint to others in their community, fostering friendly competition.
- Personalized Recommendations: Based on user data and future predictions, the platform provides actionable insights for reducing personal emissions.
- Machine Learning Predictions: Using time-series forecasting (LSTM), the platform predicts future emissions trends, helping users plan their sustainability efforts.
- Eco-points Gamification: Users are rewarded for sustainable actions with eco-points that can be redeemed for rewards, further encouraging eco-conscious behavior.


 ## DataSets Untilization 

- EPA Carbon Emissions Data      - Data from the U.S. Environmental Protection Agency (EPA) on carbon emissions across various sectors (transportation, energy, industry) to provide benchmarks for personal and community-level carbon footprints.
-  Energy Consumption Data      - Data on local and regional energy usage trends, especially from renewable and non-renewable sources, to help individuals optimize their energy consumption and make sustainable energy choices.
-  Co2_FootPrints Data               -The co2_footprints dataset is designed to track and analyze individual and community carbon footprints, supporting data-driven decision-making to combat climate change. This dataset enables users to log their activities, assess their CO2 emissions, and engage in collective actions that contribute to environmental sustainability.


## Installation & Setup
## 1. Clone the Repository:

bash

git clone https://github.com/your-username/eco-citizenship-platform.git

## 2. Frontend Setup:

bash

cd frontend/
npm install
npm start

## This will launch the frontend on localhost:3000.

## 3. Backend Setup:

bash

cd backend/
pip install -r requirements.txt
python app.py

## The Flask backend will run on localhost:5000.


## Usage :

- Track Eco-Points: Users earn eco-points for actions such as reducing energy consumption or switching to renewable energ
- View Carbon Footprint: Visualize personal and community-wide carbon emissions trends with interactive graphs.
- Receive Recommendations: Based on the user's historical data and forecasted trends, personalized recommendations are provided.


## Future Improvements

- IoT Integration: Real-time tracking of carbon emissions from smart devices such as energy meters and smart thermostats.
- Mobile App: Develop a mobile app to allow users to track their emissions and eco-points on the go.
- Enhanced Machine Learning Models: Incorporating more advanced models to provide deeper insights into emissions and energy-saving opportunities.


























## Workflow with model.pkl and scaler.pkl:

- Load the scaler from scaler.pkl to scale input data during prediction.
- Load the model from model.pkl to make predictions on scaled data.
-  Use the scaler again to inverse transform the predicted values back to their original scale.



