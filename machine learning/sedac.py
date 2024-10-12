# Import the required libraries
import requests
import folium
import folium.plugins
from folium import Map, TileLayer
from pystac_client import Client
import branca
import pandas as pd
import matplotlib.pyplot as plt

# Provide the STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# Name of the collection for SEDAC population density dataset 
collection_name = "sedac-popdensity-yeargrid5yr-v4.11"

# Fetch the collection from the STAC API
collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()

# Create a function to get the item count in a data collection
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

# Apply the function to the data collection
number_of_items = get_item_count(collection_name)

# Fetch the items in the collection
items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]

# Print the total number of items found
print(f"Found {len(items)} items")

# Examine the first item in the collection
print(items[0])

# Create a dictionary where the start datetime values are queried by year and month
items_dict = {item["properties"]["start_datetime"][:7]: item for item in items}

# Specify the asset name for this collection
asset_name = "population-density"

# Fetch the min and max values for rescaling
rescale_values = {
    "max": items_dict[list(items_dict.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
    "min": items_dict[list(items_dict.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
}

# Choose a color map for displaying the observations
color_map = "rainbow"

# Make a GET request to retrieve information for the January 2020 tile
january_2020_tile = requests.get(
    f"{RASTER_API_URL}/collections/{items_dict['2020-01']['collection']}/items/{items_dict['2020-01']['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}"
).json()

# Print the properties of the retrieved granule to the console
print(january_2020_tile)

# Make a GET request to retrieve information for the January 2000 tile
january_2000_tile = requests.get(
    f"{RASTER_API_URL}/collections/{items_dict['2000-01']['collection']}/items/{items_dict['2000-01']['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}"
).json()

# Print the properties of the retrieved granule to the console
print(january_2000_tile)

# Set initial zoom and center of map for population density layer
map_ = folium.plugins.DualMap(location=(34, -118), zoom_start=6)

# Define the first map layer (January 2020)
map_layer_2020 = TileLayer(
    tiles=january_2020_tile["tiles"][0],
    attr="GHG",
    opacity=1,
)
map_layer_2020.add_to(map_.m1)

# Define the second map layer (January 2000)
map_layer_2000 = TileLayer(
    tiles=january_2000_tile["tiles"][0],
    attr="GHG",
    opacity=1,
)
map_layer_2000.add_to(map_.m2)

# Visualize the Dual Map
map_

# Define the area of interest (Texas, USA)
texas_aoi = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "coordinates": [[
            [-95, 29],
            [-95, 33],
            [-104, 33],
            [-104, 29],
            [-95, 29]
        ]],
        "type": "Polygon",
    },
}

# Create a new map to display the generated polygon
aoi_map = Map(
    tiles="OpenStreetMap",
    location=[30, -100],
    zoom_start=6,
)

# Insert the polygon to the map
folium.GeoJson(texas_aoi, name="Texas, USA").add_to(aoi_map)

# Visualize the map
aoi_map

# Check total number of items available within the collection
items = requests.get(
    f"{STAC_API_URL}/collections/{collection_name}/items?limit=300"
).json()["features"]

# Print the total number of items found
print(f"Found {len(items)} items")

# Examine the first item in the collection
print(items[0])

# Create a function that retrieves statistics for a specific granule
def generate_stats(item, geojson):
    result = requests.post(
        f"{RASTER_API_URL}/cog/statistics",
        params={"url": item["assets"][asset_name]["href"]},
        json=geojson,
    ).json()

    return {
        **result["properties"],
        "start_datetime": item["properties"]["start_datetime"],
    }

# Generate statistics using the function within the bounding box defined by the polygon
stats = [generate_stats(item, texas_aoi) for item in items]

# Print the stats for the first item in the collection
print(stats[0])

# Create a function that converts statistics in JSON format into a pandas DataFrame
def clean_stats(stats_json) -> pd.DataFrame:
    df = pd.json_normalize(stats_json)
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]
    df["date"] = pd.to_datetime(df["start_datetime"])
    return df

# Apply the function on the stats data
df = clean_stats(stats)

# Display the stats for the first 5 granules in the collection
print(df.head(5))

# Figure size
fig = plt.figure(figsize=(20, 10))

# Plot the maximum population density
plt.plot(
    df["date"],
    df["max"],
    color="red",
)

plt.xlabel("Date")
plt.ylabel("Max Population Density")
plt.title("Max Population Density Over Time")
plt.grid()
plt.show()
