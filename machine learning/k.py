# Import necessary libraries
import requests
import folium
import folium.plugins
from folium import TileLayer
import time
import warnings
from flask import Flask, request, send_file
from flask_cors import CORS

# Suppress insecure request warnings if SSL verification is disabled
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow access from your Next.js app

# Provide the STAC and RASTER API endpoints
# The STAC API is a catalog of all the existing data collections stored in the GHG Center.
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"

# The RASTER API is used to fetch collections for visualization.
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# The collection name is used to fetch the dataset from the STAC API.
# Name of the collection for SEDAC population density dataset 
collection_name = "sedac-popdensity-yeargrid5yr-v4.11"

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
@app.route('/generate_map', methods=['POST'])
def generate_map():
    location = request.json.get("location", "California")
    collection_name = request.json.get("collection_name", "sedac-popdensity-yeargrid5yr-v4.11")
    
    # Get the number of items and fetch them
    number_of_items = get_item_count(collection_name)
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}", verify=False).json()["features"]

    # Organize the items by their start date
    items = {item["properties"]["start_datetime"][:10]: item for item in items}

    # Asset name for the population density data
    asset_name = "population_density"

    # Fetch the min and max values for rescaling
    rescale_values = {
        "max": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
        "min": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
    }

    # Color map for visualization
    color_map = "viridis"

    # Get the latest population density data
    population_density = requests.get(
        f"{RASTER_API_URL}/collections/{items[list(items.keys())[0]]['collection']}/items/{items[list(items.keys())[0]]['id']}/tilejson.json?"
        f"&assets={asset_name}&color_formula=gamma+r+1.05&colormap_name={color_map}"
        f"&rescale={rescale_values['min']},{rescale_values['max']}",
        verify=False
    ).json()

    # Create a side-by-side map with the specified location
    map_ = folium.plugins.DualMap(location=(34, -118), zoom_start=6)  # Adjust these coordinates as needed

    # Define the population density map layer and add it to the first map
    TileLayer(
        tiles=population_density["tiles"][0],
        attr="SEDAC",
        opacity=0.8
    ).add_to(map_.m1)

    # Save the map as an HTML file
    map_.save("dual_map.html")

    # Serve the map file
    return send_file("dual_map.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
