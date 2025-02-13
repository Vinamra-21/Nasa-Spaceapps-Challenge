from flask import Flask, send_file, request, jsonify
import requests
import folium
import time
import warnings
import branca
from flask_cors import CORS
from plotter2 import generate_co2_emission_graph

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

app = Flask(__name__)
CORS(app)  # Enable CORS to allow access from your Next.js app

STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name = "oco2-mip-co2budget-yeargrid-v1"

# Get the item count from STAC API
def get_item_count(collection_id):
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"
    
    while True:
        try:
            response = requests.get(items_url, verify=False, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        stac = response.json()
        count += int(stac["context"].get("returned", 0))
        next_page = [link for link in stac["links"] if link["rel"] == "next"]
        if not next_page:
            break
        items_url = next_page[0]["href"]
    
    return count

@app.route('/co2', methods=['GET'])
def generate_CO2():
    input_year = request.args.get('year', '2016')

    number_of_items = get_item_count(collection_name)
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]

    items_by_year = {item["properties"]["start_datetime"][:4]: item for item in items}

    asset_name = "ff"
    rescale_values = {"max": 450, "min": 0}
    color_map = "purd"

    if input_year in items_by_year:
        item = items_by_year[input_year]
        co2_flux = requests.get(
            f"{RASTER_API_URL}/collections/{item['collection']}/items/{item['id']}/tilejson.json?"
            f"&assets={asset_name}&color_formula=gamma+r+1.05&colormap_name={color_map}"
            f"&rescale={rescale_values['min']},{rescale_values['max']}"
        ).json()

        map_ = folium.Map(location=(34, -118), zoom_start=6)
        map_layer = folium.TileLayer(
            tiles=co2_flux["tiles"][0],
            attr="GHG",
            opacity=0.5,
        )
        map_layer.add_to(map_)

        map_file_path = f"co2_{input_year}.html"
        map_.save(map_file_path)
        
        return send_file(map_file_path)

    return jsonify({"error": f"No data available for the year {input_year}."}), 404

##############################################################################################

@app.route('/micasa', methods=['GET'])
def generate_micasa():
    # STAC and RASTER API endpoints
    STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
    RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
    collection_name = "micasa-carbonflux-daygrid-v1"
    asset_name = "rh"
    
    # Fetch all items (granules) from the collection
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit=800").json()["features"]
    items = {item["properties"]["datetime"][:10]: item for item in items}
    
    # Rescale values
    rescale_values = {
        "max": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
        "min": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
    }

    # Input the desired year from the query parameters
    year_input = request.args.get('year', default='2023')  # Default to 2016 if not provided
    date1 = f"{year_input}-01-01"  # Fetch data for January 1st of the input year

    # Fetch the tile data for the selected year
    if date1 in items:
        date1_tile = requests.get(
            f"{RASTER_API_URL}/collections/{items[date1]['collection']}/items/{items[date1]['id']}/tilejson.json?"
            f"&assets={asset_name}"
            f"&color_formula=gamma+r+1.05&colormap_name=purd"
            f"&rescale={rescale_values['min']},{rescale_values['max']}"
        ).json()

        map_ = folium.Map(location=(31.9, -99.9), zoom_start=6)

        map_layer = folium.TileLayer(
            tiles=date1_tile["tiles"][0],
            attr="GHG",
            opacity=0.8,
            name=f"{date1} Rh Level",
            overlay=True,
            legend_enabled=True
        )

        # Add the layer to the map
        map_layer.add_to(map_)

        # Add layer control to switch between layers
        folium.LayerControl(collapsed=False).add_to(map_)

        # Add colormap legend
        colormap = branca.colormap.linear.PuRd_09.scale(0, 0.3)
        colormap = colormap.to_step(index=[0, 0.07, 0.15, 0.22, 0.3])
        colormap.caption = 'Rh Values (gm Carbon/m2/daily)'
        colormap.add_to(map_)

        map_file_path = f"micasa_{date1}.html"
        map_.save(map_file_path)
        
        return send_file(map_file_path)

    else:
        return jsonify({"error": f"No data available for the year {year_input}."}), 404  # Return JSON error

##################################################################################################################
@app.route('/odiac', methods=['GET'])
def generate_odiac():
    STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
    RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
    collection_name = "odiac-ffco2-monthgrid-v2023"
    asset_name = "co2-emissions"

    number_of_items = get_item_count(collection_name)
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]
    items = {item["properties"]["start_datetime"][:7]: item for item in items}

    year_input = request.args.get('year', '2012')
    date_key = f"{year_input}-01"

    if date_key in items:
        asset_info = items[date_key]["assets"][asset_name]
        rescale_values = {
            "max": asset_info["raster:bands"][0]["histogram"]["max"],
            "min": asset_info["raster:bands"][0]["histogram"]["min"]
        }

        date_tile = requests.get(
            f"{RASTER_API_URL}/collections/{items[date_key]['collection']}/items/{items[date_key]['id']}/tilejson.json?"
            f"&assets={asset_name}"
            f"&color_formula=gamma+r+1.05&colormap_name=rainbow"
            f"&rescale={rescale_values['min']},{rescale_values['max']}"
        ).json()

        map_ = folium.Map(location=(34, -118), zoom_start=6)

        map_layer = folium.TileLayer(
            tiles=date_tile["tiles"][0],
            attr="GHG",
            opacity=0.8,
            name=f"{date_key} CO2 Emissions",
            overlay=True,
            legend_enabled=True
        )

        map_layer.add_to(map_)
        folium.LayerControl(collapsed=False).add_to(map_)

        colormap = branca.colormap.linear.RdYlGn_09.scale(rescale_values['min'], rescale_values['max'])
        colormap.caption = 'CO2 Emissions (g/m²/day)'
        colormap.add_to(map_)
        
        map_file_path = f"odiac_{date_key}.html"
        map_.save(map_file_path)
        
        return send_file(map_file_path)
    else:
        print(f"No data available for the year {year_input}.")
        return jsonify({"error": f"No data available for the year {year_input}."}), 404

##################################################################################################################
import datetime 
@app.route('/wetlands',methods=['GET'])
def generate_wetlands():

    STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
    RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

    collection_name = "lpjeosim-wetlandch4-daygrid-v2"
    asset_name = "ensemble-mean-ch4-wetlands-emissions"

    collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()

    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit=800").json()["features"]

    items = {item["properties"]["datetime"][:10]: item for item in items}

    def visualize_map(date_str):
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            # Check if the date exists in the collection
            if formatted_date not in items:
                print(f"No data available for {formatted_date}")
                return

            # Fetch tile data for the specified date
            tile_data = requests.get(
                f"{RASTER_API_URL}/collections/{items[formatted_date]['collection']}/items/{items[formatted_date]['id']}/tilejson.json?"
                f"&assets={asset_name}"
                f"&color_formula=gamma+r+1.05&colormap_name=magma"
                f"&rescale=0.0,0.0003"
            ).json()

            # Create a map centered at the specified location (California coast)
            map_ = folium.Map(location=(34, -118), zoom_start=6)

            # Define a map layer for the tile fetched
            map_layer = folium.TileLayer(
                tiles=tile_data["tiles"][0],  # Path to retrieve the tile
                attr="GHG",  # Set the attribution
                opacity=0.5,  # Adjust transparency
            )

            # Add the layer to the map
            map_layer.add_to(map_)

            # Display the map
            return map_

        except Exception as e:
            print(f"Error: {str(e)}")

    # Example: Get user input for the date
    input_date = '01/01/2024'#input("Enter the date (dd/mm/yyyy): ")
    map_ = visualize_map(input_date)

    if map_:
        map_file_path =  map_file_path = f"wetlands_{input_date}.html"
        map_.save(map_file_path)
        print("Map created successfully! Check the file 'wetland.html'.")
        return send_file(map_file_path)
###################################################################################################################
@app.route('/search', methods=['POST'])
def search_place():
    data = request.json
    place_name = data.get('place')
    print(place_name)  # Debugging output
    if not place_name:
        return jsonify({"error": "Place name is required"}), 400

    try:
        # Call the function to generate the image
        img_path = generate_co2_emission_graph(place_name)  # Ensure this returns the file path
        print(img_path)  # Debugging output
        if img_path:
            # Return the path of the saved image
            return jsonify({
                "message": f"CO2 emission graph for {place_name} generated successfully!",
                "image_url": img_path  # Use the correct image path directly
            })
        else:
            return jsonify({"error": "No valid data found for the specified location."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
###################################################################################################################

import pandas as pd
import joblib
import google.generativeai as genai
import os
from dotenv import load_dotenv

def load_model_and_theta():
    model = joblib.load('./model1.joblib')
    
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)