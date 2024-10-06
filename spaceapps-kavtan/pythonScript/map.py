
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
def generate_CO2():
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

    # Fetch the input year from query params, default to '2016' if not provided
    input_year = request.args.get('year', '2016')  # Fetch the input_year from query params
    print(f"Year requested: {input_year}")
    
    # Check if the requested year exists in the dataset
    if input_year in items_by_year:
        item = items_by_year[input_year]

        # Fetch CO2 flux data for the input year
        co2_flux = requests.get(
            f"{RASTER_API_URL}/collections/{item['collection']}/items/{item['id']}/tilejson.json?"
            f"&assets={asset_name}"
            f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
            f"&rescale={rescale_values['min']},{rescale_values['max']}"
        ).json()

        # Set the location (latitude and longitude of the area of interest, e.g., California)
        map_ = folium.Map(location=(34, -118), zoom_start=6)

        # Define the map layer for the chosen year
        map_layer = folium.TileLayer(
            tiles=co2_flux["tiles"][0],  # Path to the tile
            attr="GHG",  # Attribution
            opacity=0.5,  # Transparency
        )

        # Add the layer to the map
        map_layer.add_to(map_)

        # Save the map as an HTML file with the year as part of the filename
        map_file_path = f"E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/spaceapps-kavtan/public/co2_{input_year}.html"
        map_.save(map_file_path)
        
        print(f"Map for {input_year} has been saved as '{map_file_path}'.")

        return send_file(map_file_path)

    else:
        print(f"No data available for the year {input_year}.")
        return jsonify({"error": f"No data available for the year {input_year}."}), 404


##############################################################################################
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name = "micasa-carbonflux-daygrid-v1"
asset_name = "rh"
# Function to fetch the number of items dynamically
def get_item_count1(collection_name):
    try:
        response = requests.get(f"{STAC_API_URL}/collections/{collection_name}")
        response.raise_for_status()
        return response.json()["extent"]["spatial"]["bbox"][0]  # Example: Replace with the actual logic to fetch the count
    except requests.exceptions.RequestException as e:
        print(f"Error fetching item count: {e}")
        return 0

@app.route('/micasa', methods=['GET'])
def generate_micasa():


    # Fetch the number of items dynamically based on the collection
    number_of_items = get_item_count1(collection_name)
    if number_of_items == 0:
        return jsonify({"error": "Unable to fetch item count from collection."}), 500

    # Fetch all items (granules) from the collection
    try:
        response = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}")
        response.raise_for_status()
        items = response.json()["features"]
        items = {item["properties"]["datetime"][:10]: item for item in items}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching items: {e}")
        return jsonify({"error": "Unable to fetch items from collection."}), 500

    # Set rescale values from the first item in the dataset
    first_item = next(iter(items.values()), None)
    if not first_item:
        return jsonify({"error": "No items found in the collection."}), 404

    rescale_values = {
        "max": first_item["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
        "min": first_item["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
    }

    # Fetch the input year from query params, default to '2023' if not provided
    input_year = request.args.get('year', '2023')
    date1 = f"{input_year}-01-01"  # Fetch data for January 1st of the input year

    print(f"Year requested: {input_year}")

    # Fetch the tile data for the selected year
    if date1 in items:
        try:
            date1_tile = requests.get(
                f"{RASTER_API_URL}/collections/{items[date1]['collection']}/items/{items[date1]['id']}/tilejson.json?"
                f"&assets={asset_name}"
                f"&color_formula=gamma+r+1.05&colormap_name=purd"
                f"&rescale={rescale_values['min']},{rescale_values['max']}"
            ).json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tile data: {e}")
            return jsonify({"error": f"Unable to fetch tile data for the year {input_year}."}), 500

        # Set initial zoom and center of map
        map_ = folium.Map(location=(31.9, -99.9), zoom_start=6)

        # Define map layer with Rh level for the tile fetched for the selected year
        map_layer = folium.TileLayer(
            tiles=date1_tile["tiles"][0],
            attr="GHG",
            opacity=0.8,
            name=f"{date1} Rh Level",
            overlay=True,
            legend_name='Rh Levels',
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

        # Save the map as an HTML file
        map_file_path = f"E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/spaceapps-kavtan/public/micasa_{input_year}.html"
        map_.save(map_file_path)

        print(f"Map for {input_year} has been saved as 'micasa_{input_year}.html'.")
        return send_file(map_file_path)
    else:
        print(f"No data available for the year {input_year}.")
        return jsonify({"error": f"No data available for the year {input_year}."}), 404

#####################################################################################################
from datetime import datetime
@app.route('/wetlands',methods=['GET'])
def generate_wetlands():
        
    # STAC and RASTER API endpoints
    STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
    RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

    # Collection and asset details
    collection_name = "lpjeosim-wetlandch4-daygrid-v2"
    asset_name = "ensemble-mean-ch4-wetlands-emissions"

    # Fetch the collection from the STAC API
    collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()

    # Fetch the collection items (granules)
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit=800").json()["features"]

    # Convert items to a dictionary where the key is the date
    items = {item["properties"]["datetime"][:10]: item for item in items}

    # Function to visualize data for a given date
    def visualize_map(date_str):
        try:
            # Convert the input date string to the correct format (yyyy-mm-dd)
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
    input_date = "01/01/2023" #input("Enter the date (dd/mm/yyyy): ")
    map_ = visualize_map(input_date)

    # Show the map if it's successfully created
    if map_:
        map_file_path = rf"E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/spaceapps-kavtan/public/wetlands_{input_date}.html"
        map_.save(map_file_path)
        print("Map created successfully! Check the file 'wetland.html'.")
        return send_file(map_file_path)
# #####################################################################################################################
import requests
import folium
import branca
from flask import request, send_file

@app.route('/odiac', methods=['GET'])
def generate_odiac():
    # STAC and RASTER API endpoints
    STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
    RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
    collection_name = "odiac-ffco2-monthgrid-v2023"
    asset_name = "co2-emissions"

    # Function to fetch items from the STAC API
    def get_item_count(collection_id):
        count = 0
        items_url = f"{STAC_API_URL}/collections/{collection_id}/items"
        while True:
            response = requests.get(items_url)
            if not response.ok:
                print("Error getting items")
                exit()
            stac = response.json()
            count += int(stac["context"].get("returned", 0))
            next_links = [link for link in stac["links"] if link["rel"] == "next"]
            if not next_links:
                break
            items_url = next_links[0]["href"]
        return count

    # Fetch all items (granules) from the collection
    number_of_items = get_item_count(collection_name)
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]
    items = {item["properties"]["start_datetime"][:7]: item for item in items}

    # Get the year from query parameters (e.g., '2020' for '2020-01')
    year_input = request.args.get('date', '2020')  # Default to 2020 if not provided
    date_key = f"{year_input}-01"  # Fetch data for January of the input year

    # Check if data is available for the selected year
    if date_key in items:
        asset_info = items[date_key]["assets"][asset_name]
        rescale_values = {
            "max": asset_info["raster:bands"][0]["histogram"]["max"],
            "min": asset_info["raster:bands"][0]["histogram"]["min"]
        }

        # Fetch the tile data for the selected year
        date_tile = requests.get(
            f"{RASTER_API_URL}/collections/{items[date_key]['collection']}/items/{items[date_key]['id']}/tilejson.json?"
            f"&assets={asset_name}"
            f"&color_formula=gamma+r+1.05&colormap_name=rainbow"
            f"&rescale={rescale_values['min']},{rescale_values['max']}"
        ).json()

        # Set initial zoom and center of the map
        map_ = folium.Map(location=(34, -118), zoom_start=6)

        # Define map layer with CO2 emissions for the tile fetched for the selected year
        map_layer = folium.TileLayer(
            tiles=date_tile["tiles"][0],
            attr="GHG",
            opacity=0.8,
            name=f"{date_key} CO2 Emissions",
            overlay=True,
            legend_enabled=True
        )

        # Add the layer to the map
        map_layer.add_to(map_)

        # Add layer control to switch between layers
        folium.LayerControl(collapsed=False).add_to(map_)

        # Add colormap legend
        colormap = branca.colormap.linear.RdYlGn_09.scale(rescale_values['min'], rescale_values['max'])
        colormap.caption = 'CO2 Emissions (g/m²/day)'
        colormap.add_to(map_)

        # Save the map to a file
        map_file_path = r"E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/spaceapps-kavtan/public/odiac.html"
        map_.save(map_file_path)
        print("Map created successfully! Check the file 'odiac.html'.")
        return send_file(map_file_path)

    else:
        return f"No data available for the year {year_input}.", 404

##################################################################################################################
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