from flask import Flask, request, jsonify
import pandas as pd
import joblib
import google.generativeai as genai
from flask_cors import CORS
import os
from dotenv import load_dotenv
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

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
        percent_impact = (new_emissions - base_emissions) / base_emissions * 100
        
        results[column] = {
            "original_value": base_data[column].values[0],
            "modified_value": modified_data[column].values[0],
            "emissions_change": new_emissions - base_emissions,
            "percent_impact": percent_impact
        }
    
    return base_emissions, results

def print_sensitivity_results(base_emissions, results):
    superstr = f"Base net carbon emissions: {base_emissions:.2f}\nSensitivity Analysis Results:"
    
    sorted_results = sorted(results.items(), key=lambda x: abs(x[1]['percent_impact']), reverse=True)
    
    for column, data in sorted_results:
        superstr += f"\n{column}:"
        superstr += f"  Original value: {data['original_value']:.2f}"
        superstr += f"  Modified value: {data['modified_value']:.2f}"
        superstr += f"  Emissions change: {data['emissions_change']:.2f}"
        superstr += f"  Percent impact: {data['percent_impact']:.2f}%"

    return superstr

def generate_output(data):
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    input_text = (
        "You are a model that analyses the impact of land use and population on carbon emissions. "
        "You are connected to a machine learning model that accepts cropland, grazing land, forest land, "
        "fishing ground, builtup land, and population to predict carbon dioxide emissions. "
        "This machine learning model runs a sensitivity check by incrementing each attribute by 5% and "
        "seeing how the emission prediction changes. I need you to understand that data, summarise it "
        "and explain it. Additionally, explain what policies (relating to land and population) should be "
        "followed to best have an impact on carbon dioxide emissions. The units of carbon dioxide emissions "
        "are dioxide per square meter per year (g CO₂/m²/yr) and the land data is hectares. The sensitivity "
        "analysis results are:" + data
    )

    response = model.generate_content(input_text)
    return response.text

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    base_data = pd.DataFrame({
        'cropLand': [data['cropLand']],
        'grazingLand': [data['grazingLand']],
        'forestLand': [data['forestLand']],
        'fishingGround': [data['fishingGround']],
        'builtupLand': [data['builtupLand']],
        'population': [data['population']],
    })

    model, theta = load_model_and_theta()
    base_emissions, results = sensitivity_analysis(model, theta, base_data)
    output = print_sensitivity_results(base_emissions, results)
    generated_output = generate_output(output)

    return jsonify({"sensitivity_analysis": output, "generated_explanation": generated_output})

##################################################################################################################

model2 = joblib.load('model2.joblib')

theta = {
    "cropLand": {"mean": 11611656.9279, "std": 27400727.8380},
    "grazingLand": {"mean": 4581758.5791, "std": 13076951.6274},
    "fishingGround": {"mean": 2841642.2978, "std": 6823832.052},
    "builtupLand": {"mean": 1696530.7444, "std": 4737441.2535},
    "Population": {"mean": 24824301.3865, "std": 86332026.1835},
    "carbon": {"mean": 27416994.6602, "std": 770980962.4080},
    "forestLand": {"mean": 7115808.9516, "std": 16629948.2851}
}

def normalize_input2(input_data):
    normalized_data = input_data.copy()
    for col in normalized_data.columns:
        normalized_data[col] = (normalized_data[col] - theta[col]['mean']) / theta[col]['std']
    return normalized_data

def denormalize_output2(prediction):
    return prediction * theta['carbon']['std'] + theta['carbon']['mean']

def predict_emissions2(input_data):
    normalized_input = normalize_input2(input_data)
    prediction = model2.predict(normalized_input)[0]
    return denormalize_output2(prediction)

def sensitivity_analysis2(base_data, percent_change=5):
    base_emissions = predict_emissions2(base_data)
    results = {}

    for column in base_data.columns:
        modified_data = base_data.copy()
        modified_data[column] *= (1 + percent_change / 100)
        
        new_emissions = predict_emissions2(modified_data)
        percent_impact = -(new_emissions - base_emissions) / base_emissions * 100
        
        results[column] = {
            "original_value": base_data[column].values[0],
            "modified_value": modified_data[column].values[0],
            "emissions_change": -new_emissions + base_emissions,
            "percent_impact": percent_impact
        }
    
    return base_emissions, results

def format_sensitivity_results2(base_emissions, results):
    output = f"Base net methane emissions: {base_emissions:.2f}\nSensitivity Analysis Results:"
    
    sorted_results = sorted(results.items(), key=lambda x: abs(x[1]['percent_impact']), reverse=True)
    
    for column, data in sorted_results:
        output += f"\n{column}:"
        output += f"  Original value: {data['original_value']:.2f}"
        output += f"  Modified value: {data['modified_value']:.2f}"
        output += f"  Emissions change: {data['emissions_change']:.2f}"
        output += f"  Percent impact: {data['percent_impact']:.2f}%"

    return output

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    base_data = pd.DataFrame({k: [v] for k, v in data.items()})
    base_data = base_data[model2.feature_names_in_]
    
    base_emissions, results = sensitivity_analysis2(base_data)
    output = format_sensitivity_results2(base_emissions, results)
    
    return jsonify({
        "base_emissions": base_emissions,
        "results": results,
        "output": output
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)  