from flask import Flask, request, jsonify
import pandas as pd
import joblib
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model and theta values globally to avoid reloading on each request
model = joblib.load('E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/App3/model2.joblib')

theta = {
    "cropLand": {"mean": 11611656.9279, "std": 27400727.8380},
    "grazingLand": {"mean": 4581758.5791, "std": 13076951.6274},
    "fishingGround": {"mean": 2841642.2978, "std": 6823832.052},
    "builtupLand": {"mean": 1696530.7444, "std": 4737441.2535},
    "Population": {"mean": 24824301.3865, "std": 86332026.1835},
    "carbon": {"mean": 27416994.6602, "std": 770980962.4080},
    "forestLand": {"mean": 7115808.9516, "std": 16629948.2851}
}

def normalize_input(input_data):
    normalized_data = input_data.copy()
    for col in normalized_data.columns:
        normalized_data[col] = (normalized_data[col] - theta[col]['mean']) / theta[col]['std']
    return normalized_data

def denormalize_output(prediction):
    return prediction * theta['carbon']['std'] + theta['carbon']['mean']

def predict_emissions(input_data):
    normalized_input = normalize_input(input_data)
    prediction = model.predict(normalized_input)[0]
    return denormalize_output(prediction)

def sensitivity_analysis(base_data, percent_change=5):
    base_emissions = predict_emissions(base_data)
    results = {}

    for column in base_data.columns:
        modified_data = base_data.copy()
        modified_data[column] *= (1 + percent_change / 100)
        
        new_emissions = predict_emissions(modified_data)
        percent_impact = -(new_emissions - base_emissions) / base_emissions * 100
        
        results[column] = {
            "original_value": base_data[column].values[0],
            "modified_value": modified_data[column].values[0],
            "emissions_change": -new_emissions + base_emissions,
            "percent_impact": percent_impact
        }
    
    return base_emissions, results

def format_sensitivity_results(base_emissions, results):
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
    base_data = pd.DataFrame(data)
    base_data = base_data[model.feature_names_in_]
    
    base_emissions, results = sensitivity_analysis(base_data)
    output = format_sensitivity_results(base_emissions, results)
    
    return jsonify({
        "base_emissions": base_emissions,
        "results": results,
        "output": output
    })

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Change to run on port 5002