
import requests
import folium
import folium.plugins
import time
import warnings
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from matplotlib import pyplot as plt
from plotter2 import generate_co2_emission_graph  # Make sure this function is defined correctly

# Suppress insecure request warnings if SSL verification is disabled
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow access from your Next.js app


# Provide the STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name = "oco2-mip-co2budget-yeargrid-v1"

# Define the function to get item count
def get_item_count(collection_id):
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"
    
    while True:
        try:
            response = requests.get(items_url, verify=False, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
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
def generate_map():
    # Fetch the number of items
    number_of_items = get_item_count(collection_name)
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]

    # Create a dictionary where the start datetime values for each granule are more explicitly queried by year
    items_by_year = {item["properties"]["start_datetime"][:4]: item for item in items}
    
    # Set the asset name for fossil fuel ("ff")
    asset_name = "ff"
    # Rescale values for visualization (adjusted as per GHG Center scale)
    rescale_values = {"max": 450, "min": 0}
    color_map = "purd"

    # Default year is 2016 if not provided (could be made dynamic based on input)
    input_year = '2016'

    # Check if the year exists in the dataset
    if input_year in items_by_year:
        item = items_by_year[input_year]

        # Fetch CO2 flux data for the input year
        co2_flux = requests.get(
            f"{RASTER_API_URL}/collections/{item['collection']}/items/{item['id']}/tilejson.json?"
            f"&assets={asset_name}"
            f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
            f"&rescale={rescale_values['min']},{rescale_values['max']}"
        ).json()

        # Set the location (latitude and longitude of the area of interest, California here)
        map_ = folium.Map(location=(34, -118), zoom_start=6)

        # Define the map layer for the chosen year
        map_layer = folium.TileLayer(
            tiles=co2_flux["tiles"][0],  # Path to the tile
            attr="GHG",  # Attribution
            opacity=0.5,  # Transparency
        )

        # Add the layer to the map
        map_layer.add_to(map_)

        # Save the map as an HTML file
        map_file_path = f"E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/spaceapps-kavtan/public/co2{input_year}.html"
        map_.save(map_file_path)
        
        print(f"Map for {input_year} has been saved as 'co2.html'.")

        return send_file(map_file_path)

    else:
        print(f"No data available for the year {input_year}.")
        return jsonify({"error": f"No data available for the year {input_year}."}), 404

########################################################################################################

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)