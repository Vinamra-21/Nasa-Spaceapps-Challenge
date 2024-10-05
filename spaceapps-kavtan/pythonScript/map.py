
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

# API endpoints for STAC and RASTER
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name = "tm54dvar-ch4flux-monthgrid-v1"

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

@app.route('/map', methods=['GET'])
def generate_map():
    number_of_items = get_item_count(collection_name)
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}", verify=False).json()["features"]

    # Organize items by their start date
    items = {item["properties"]["start_datetime"][:10]: item for item in items}
    
    asset_name = "fossil"
    
    rescale_values = {
        "max": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
        "min": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
    }

    color_map = "purd"

    # Fetch CH₄ flux data
    ch4_flux_1 = requests.get(
        f"{RASTER_API_URL}/collections/{items['2016-12-01']['collection']}/items/{items['2016-12-01']['id']}/tilejson.json?"
        f"&assets={asset_name}&color_formula=gamma+r+1.05&colormap_name={color_map}"
        f"&rescale={rescale_values['min']},{rescale_values['max']}",
        verify=False
    ).json()

    ch4_flux_2 = requests.get(
        f"{RASTER_API_URL}/collections/{items['1999-12-01']['collection']}/items/{items['1999-12-01']['id']}/tilejson.json?"
        f"&assets={asset_name}&color_formula=gamma+r+1.05&colormap_name={color_map}"
        f"&rescale={rescale_values['min']},{rescale_values['max']}",
        verify=False
    ).json()

    # Create a side-by-side map of California
    map_ = folium.plugins.DualMap(location=(34, -118), zoom_start=6)

    # Add layers to the map
    folium.TileLayer(tiles=ch4_flux_1["tiles"][0], attr="GHG", opacity=0.8).add_to(map_.m1)
    folium.TileLayer(tiles=ch4_flux_2["tiles"][0], attr="GHG", opacity=0.8).add_to(map_.m2)

    # Save the map as an HTML file
    map_file_path = "E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/spaceapps-kavtan\public\dual_map.html"  # Use a relative path
    map_.save(map_file_path)

    return send_file(map_file_path)


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