# Import necessary libraries
import requests
import folium
import folium.plugins
from folium import TileLayer
import time
import warnings
from flask import Flask, send_file, request, jsonify  # Import request and jsonify
from flask_cors import CORS

# Suppress insecure request warnings if SSL verification is disabled
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow access from your Next.js app

# API endpoints for STAC and RASTER
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# Name of the collection (TM5 CH₄ inverse flux dataset)
collection_name = "tm54dvar-ch4flux-monthgrid-v1"

# Function to count the number of items in the collection, with retry and timeout handling
def get_item_count(collection_id):
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"
    
    while True:
        try:
            # Make the request with a timeout and SSL verification disabled
            response = requests.get(items_url, verify=False, timeout=10)
            response.raise_for_status()  # Raise exception for bad responses
        except requests.exceptions.RequestException as e:
            # Retry if there is any network-related error
            print(f"Error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        # Process the response if successful
        stac = response.json()
        count += int(stac["context"].get("returned", 0))

        # Look for the next page of results
        next = [link for link in stac["links"] if link["rel"] == "next"]
        if not next:
            break
        items_url = next[0]["href"]
    
    return count

# Flask route to generate and serve the dual map
@app.route('/')
def generate_map():
    print("1 done")
    # Get the number of items and fetch them
    number_of_items = get_item_count(collection_name)
    print("1.5 done")
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}", verify=False).json()["features"]
    print("2 done")
    # Organize the items by their start date
    items = {item["properties"]["start_datetime"][:10]: item for item in items}
    print("3 done")
    # Asset name for the CH₄ fossil fuel flux data
    asset_name = "fossil"
    print("4 done")
    # Fetch the min and max values for rescaling
    rescale_values = {
        "max": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
        "min": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
    }
    print("5 done")

    # Color map for visualization
    color_map = "purd"
    print("6 done")

    # Get the 2016 CH₄ flux data
    ch4_flux_1 = requests.get(
        f"{RASTER_API_URL}/collections/{items['2016-12-01']['collection']}/items/{items['2016-12-01']['id']}/tilejson.json?"
        f"&assets={asset_name}&color_formula=gamma+r+1.05&colormap_name={color_map}"
        f"&rescale={rescale_values['min']},{rescale_values['max']}",
        verify=False
    ).json()
    print("7 done")

    # Get the 1999 CH₄ flux data
    ch4_flux_2 = requests.get(
        f"{RASTER_API_URL}/collections/{items['1999-12-01']['collection']}/items/{items['1999-12-01']['id']}/tilejson.json?"
        f"&assets={asset_name}&color_formula=gamma+r+1.05&colormap_name={color_map}"
        f"&rescale={rescale_values['min']},{rescale_values['max']}",
        verify=False
    ).json()
    print("8 done")

    # Create a side-by-side map of California
    map_ = folium.plugins.DualMap(location=(34, -118), zoom_start=6)
    print("9 done")

    # Define the 2016 map layer and add it to the first map
    TileLayer(
        tiles=ch4_flux_1["tiles"][0],
        attr="GHG",
        opacity=0.8
    ).add_to(map_.m1)
    print("10 done")

    # Define the 1999 map layer and add it to the second map
    TileLayer(
        tiles=ch4_flux_2["tiles"][0],
        attr="GHG",
        opacity=0.8
    ).add_to(map_.m2)
    print("11 done")

    # Save the map as an HTML file
    map_.save("E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/spaceapps-kavtan/public/dual_map.html")
    print("12 done")
    # Serve the map file
    return send_file("E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/spaceapps-kavtan/public/dual_map.html")

from flask import Flask, request, jsonify
from flask_cors import CORS
import finder
import matplotlib.pyplot as plt
import io
import base64

# Import your function (assuming it's in a file called co2_emission.py)
from plotter2 import generate_co2_emission_graph

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow access from your Next.js app

@app.route('/search', methods=['POST'])
def search_place():
    # Get the place name from the request JSON body
    data = request.json
    place_name = data.get('place')
    
    if not place_name:
        return jsonify({"error": "Place name is required"}), 400
    
    try:
        # Generate CO2 emission graph for the given location
        img = generate_co2_emission_graph(place_name)

        # Return the graph as a base64-encoded image string
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        return jsonify({"message": f"CO2 emission graph for {place_name} generated successfully!", "image": img_base64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

