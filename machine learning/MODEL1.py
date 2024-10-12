import pandas as pd
import numpy as np
import joblib
import google.generativeai as genai

def load_model_and_theta():
    model = joblib.load('model1.joblib')
    
    theta = {
        "cropLand": {"mean": 20198508.13312177, "std": 50714883.562947996},
        "grazingLand": {"mean": 5832458.223382353, "std": 14554527.9538871},
        "forestLand": {"mean": 10911793.038451144, "std": 29114548.94593724},
        "fishingGround": {"mean": 3683135.6772812237, "std": 7723749.890470839},
        "builtupLand": {"mean": 2739420.850624563, "std": 7208179.292714253},
        "population": {"mean": 41867338.08809524, "std": 123268956.5296485},
        "netCarbonEmissions": {"mean": 273.37739993008654, "std": 715.6966236994639}
    }
    
    return model, theta

def normalize_input(input_data, theta):
    normalized_data = input_data.copy()
    for col in normalized_data.columns:
        normalized_data[col] = (normalized_data[col] - theta[col]['mean']) / theta[col]['std']
    return normalized_data

def denormalize_output(prediction, theta):
    return prediction * theta['netCarbonEmissions']['std'] + theta['netCarbonEmissions']['mean']

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
    superstr += f"Base net carbon emissions: {base_emissions:.2f}"
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
    
    base_data = pd.DataFrame({
        'cropLand': [int(input("Enter crop land area: "))],
        'grazingLand': [6000000],
        'forestLand': [11000000],
        'fishingGround': [3700000],
        'builtupLand': [2700000],
        'population': [40000000]
    })
    
    base_emissions, results = sensitivity_analysis(model, theta, base_data)
    output = print_sensitivity_results(base_emissions, results)
    generate_output(output)

def generate_output(data):
    genai.configure(api_key="AIzaSyAQ1oUSI5xhsY03Bo8VsV-o4ilnVKCOrT4")
    model = genai.GenerativeModel("gemini-1.5-flash")
    input = "You are a model that analyses the impact of land use and population on carbon emissions. You are connected to a machine learning model that accepts cropland, grazing land, forest land, fishing ground, builtup land, and population to predict carbon dioxide emissions. This machine learning model runs a sensitivity check by incrementing each attribute by 5% and seeing how the emission prediction changes. I need you to understand that data, summarise it and explain it. Additionally, explain what policies (relating to land and population) should be followed to best have an impact on carbon dioxide emissions. The sensitivity analysis results are:" + data

    response = model.generate_content(input)
    print(response.text)

if __name__ == "__main__":
    main()