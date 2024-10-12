import pandas as pd
import numpy as np
import joblib
import google.generativeai as genai
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the model
model = joblib.load('model2.joblib')

# Sensitivity analysis and API integration
def load_model_and_theta():
    theta = {
        "cropLand": {"mean": 11611656.9279, "std": 27400727.8380},
        "grazingLand": {"mean": 4581758.5791, "std": 13076951.6274},
        "fishingGround": {"mean": 2841642.2978, "std": 6823832.052},
        "builtupLand": {"mean": 1696530.7444, "std": 4737441.2535},
        "Population": {"mean": 24824301.3865, "std": 86332026.1835},
        "carbon": {"mean": 27416994.6602, "std": 770980962.4080},
        "forestLand": {"mean": 7115808.9516, "std": 16629948.2851}  # Add forestLand mean and std here
    }

    return model, theta

def normalize_input(input_data, theta):
    normalized_data = input_data.copy()
    for col in normalized_data.columns:
        normalized_data[col] = (normalized_data[col] - theta[col]['mean']) / theta[col]['std']
    return normalized_data

def denormalize_output(prediction, theta):
    return prediction * theta['carbon']['std'] + theta['carbon']['mean']

def predict_emissions(model, theta, input_data):
    normalized_input = normalize_input(input_data, theta)
    prediction = model.predict(normalized_input)[0]
    return denormalize_output(prediction, theta)

def sensitivity_analysis(model, theta, base_data, percent_change=5):
    base_emissions = predict_emissions(model, theta, base_data)
    results = {}

    for column in base_data.columns:
        modified_data = base_data.copy()
        modified_data[column] *= (1 + percent_change / 100)
        
        new_emissions = predict_emissions(model, theta, modified_data)
        percent_impact = -(new_emissions - base_emissions) / base_emissions * 100
        
        results[column] = {
            "original_value": base_data[column].values[0],
            "modified_value": modified_data[column].values[0],
            "emissions_change": -new_emissions + base_emissions,
            "percent_impact": percent_impact
        }
    
    return base_emissions, results

def print_sensitivity_results(base_emissions, results):
    superstr = """""" 
    superstr += f"Base net methane emissions: {base_emissions:.2f}"
    superstr += "\nSensitivity Analysis Results:"
    
    sorted_results = sorted(results.items(), key=lambda x: abs(x[1]['percent_impact']), reverse=True)
    
    for column, data in sorted_results:
        superstr += f"\n{column}:"
        superstr += f"  Original value: {data['original_value']:.2f}"
        superstr += f"  Modified value: {data['modified_value']:.2f}"
        superstr += f"  Emissions change: {data['emissions_change']:.2f}"
        superstr += f"  Percent impact: {data['percent_impact']:.2f}%"

    return superstr

def main():
    model, theta = load_model_and_theta()
    
    # Input data
    base_data = pd.DataFrame({
        'cropLand': [int(input('Enter cropLand: '))],
        'grazingLand': [int(input('Enter grazingLand: '))],
        'fishingGround': [int(input('Enter fishingGround: '))],
        'builtupLand': [int(input('Enter buildUpLand: '))],
        'Population': [int(input('Enter Population: '))],
        'forestLand': [int(input('Enter forestLand: '))]  
    })
    
    # Reorder the base_data columns to match the model's feature order
    base_data = base_data[model.feature_names_in_]
    
    # Perform sensitivity analysis
    base_emissions, results = sensitivity_analysis(model, theta, base_data)
    output = print_sensitivity_results(base_emissions, results)
    generate_output(output)

def generate_output(data):
    genai.configure(api_key="AIzaSyAQ1oUSI5xhsY03Bo8VsV-o4ilnVKCOrT4")
    model = genai.GenerativeModel("gemini-1.5-flash")
    input = "You are a model that analyses the impact of land use and population on methane emissions. The sensitivity analysis results are:" + data

    response = model.generate_content(input)
    print(response.text)

if __name__ == "__main__":
    main()
