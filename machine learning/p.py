import requests
import folium
import folium.plugins
from folium import Map, TileLayer
import pandas as pd
import matplotlib.pyplot as plt

# STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name = "sedac-popdensity-yeargrid5yr-v4.11"

# Fetch the collection from the STAC API
collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()

# Function to count items in a collection
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
        next_url = [link for link in stac["links"] if link["rel"] == "next"]

        if not next_url:
            break
        
        items_url = next_url[0]["href"]
    
    return count

# Get item count
number_of_items = get_item_count(collection_name)

# Fetch items
items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]

# Print total number of items found
print(f"Found {len(items)} items")

# Create a dictionary of items by start datetime
items = {item["properties"]["start_datetime"][:7]: item for item in items} 

# Define asset name and fetch min/max values
asset_name = "population-density"
rescale_values = {
    "max": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
    "min": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
}

# Set color map
color_map = "rainbow"

# Fetch tile for January 2020
january_2020_tile = requests.get(
    f"{RASTER_API_URL}/collections/{items['2020-01']['collection']}/items/{items['2020-01']['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}"
).json()

# Fetch tile for January 2000
january_2000_tile = requests.get(
    f"{RASTER_API_URL}/collections/{items['2000-01']['collection']}/items/{items['2000-01']['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}"
).json()

# Check for tiles key in the response
if "tiles" not in january_2020_tile or "tiles" not in january_2000_tile:
    print("Error: Tiles not found in the response for one of the years.")
else:
    # Set up dual map for visualization
    map_ = folium.plugins.DualMap(location=(34, -118), zoom_start=6)

    # Add 2020 layer
    TileLayer(tiles=january_2020_tile["tiles"][0], attr="GHG", opacity=1).add_to(map_.m1)
    # Add 2000 layer
    TileLayer(tiles=january_2000_tile["tiles"][0], attr="GHG", opacity=1).add_to(map_.m2)

    # Display the dual map
    map_.save("dual_map.html")
    print("Dual map saved as 'dual_map.html'.")

# Define Texas Area of Interest (AOI)
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

# Create map for AOI
aoi_map = Map(location=[30, -100], zoom_start=6)
folium.GeoJson(texas_aoi, name="Texas, USA").add_to(aoi_map)

# Save AOI map
aoi_map.save("aoi_map.html")
print("AOI map saved as 'aoi_map.html'.")

# Fetch items again to check total number
items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit=300").json()["features"]
print(f"Found {len(items)} items")

# Function to generate statistics for a granule
def generate_stats(item, geojson):
    result = requests.post(
        f"{RASTER_API_URL}/cog/statistics",
        params={"url": item["assets"][asset_name]["href"]},
        json=geojson,
    ).json()
    
    return {**result["properties"], "start_datetime": item["properties"]["start_datetime"]}

# Generate statistics for Texas AOI
stats = [generate_stats(item, texas_aoi) for item in items]

# Function to clean statistics into DataFrame
def clean_stats(stats_json) -> pd.DataFrame:
    df = pd.json_normalize(stats_json)
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]
    df["date"] = pd.to_datetime(df["start_datetime"])
    return df

# Clean stats and display first 5 rows
df = clean_stats(stats)
print(df.head(5))

# Plotting the population density over the years
fig = plt.figure(figsize=(20, 10))
plt.plot(df["date"], df["max"], color="red", linestyle="-", linewidth=0.5, label="Population density over the years")
plt.legend()
plt.xlabel("Years")
plt.ylabel("Population Density")
plt.title("Population Density over Texas, Dallas (2000-2020)")

# Add data citation
plt.text(
    df["date"].iloc[0], 
    df["max"].max(), 
    "Source: SEDAC Population Density Dataset", 
    fontsize=12, 
    ha='center'
)
plt.show()