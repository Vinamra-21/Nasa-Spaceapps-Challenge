import requests
import folium
import folium.plugins
from folium import Map, TileLayer
from pystac_client import Client
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import json

# Provide the STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# Name of the collection for CEOS National Top-Down CO₂ Budgets dataset 
collection_name = "oco2-mip-co2budget-yeargrid-v1"

# Fetch the collection from the STAC API
collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()

def get_item_count(collection_id):
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"
    while True:
        response = requests.get(items_url)
        if not response.ok:
            print("error getting items")
            exit()
        stac = response.json()
        count += int(stac["context"].get("returned", 0))
        next = [link for link in stac["links"] if link["rel"] == "next"]
        if not next:
            break
        items_url = next[0]["href"]
    return count

number_of_items = get_item_count(collection_name)

items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]
print(f"Found {len(items)} items")

items = {item["properties"]["start_datetime"]: item for item in items} 

asset_name = "ff" #fossil fuel

# Hardcoding the min and max values to match the scale in the GHG Center dashboard
rescale_values = {"max": 450, "min": 0}

color_map = "PuRd"

# Function to safely get API response and handle errors
def get_api_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print(f"URL: {url}")
        print(f"Response content: {response.text}")
        return None

# 2020
co2_flux_1_url = (
    f"{RASTER_API_URL}/collections/{items[list(items.keys())[0]]['collection']}/items/{items[list(items.keys())[0]]['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}"
)
co2_flux_1 = get_api_response(co2_flux_1_url)

# 2019
co2_flux_2_url = (
    f"{RASTER_API_URL}/collections/{items[list(items.keys())[1]]['collection']}/items/{items[list(items.keys())[1]]['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}"
)
co2_flux_2 = get_api_response(co2_flux_2_url)

# Print API response information for debugging
print("API Response for 2020:")
print(json.dumps(co2_flux_1, indent=2))
print("\nAPI Response for 2019:")
print(json.dumps(co2_flux_2, indent=2))

# Check if 'tiles' key exists before accessing it
if co2_flux_1 and 'tiles' in co2_flux_1:
    print("2020 Tile URL:", co2_flux_1["tiles"][0])
else:
    print("Error: 'tiles' key not found in 2020 data")

if co2_flux_2 and 'tiles' in co2_flux_2:
    print("2019 Tile URL:", co2_flux_2["tiles"][0])
else:
    print("Error: 'tiles' key not found in 2019 data")

# Set the initial zoom level and center of map for both tiles
map_ = folium.plugins.DualMap(location=(34, -118), zoom_start=6)

# For 2020 data
if co2_flux_1 and 'tiles' in co2_flux_1:
    folium.TileLayer(
        tiles=co2_flux_1["tiles"][0],
        attr="GHG Center 2020",
        name="CO2 Flux 2020",
        overlay=True,
        control=True,
        opacity=0.7,
    ).add_to(map_.m1)

# For 2019 data
if co2_flux_2 and 'tiles' in co2_flux_2:
    folium.TileLayer(
        tiles=co2_flux_2["tiles"][0],
        attr="GHG Center 2019",
        name="CO2 Flux 2019",
        overlay=True,
        control=True,
        opacity=0.7,
    ).add_to(map_.m2)

# Add layer controls
folium.LayerControl().add_to(map_.m1)
folium.LayerControl().add_to(map_.m2)

# Add colormap
colormap = plt.cm.get_cmap(color_map)
colors = [matplotlib.colors.rgb2hex(colormap(i)[:3]) for i in range(colormap.N)]

colormap = folium.LinearColormap(
    colors=colors,
    vmin=rescale_values['min'],
    vmax=rescale_values['max'],
    caption='CO2 Flux (g C m-2 day-1)'
)
colormap.add_to(map_.m1)
colormap.add_to(map_.m2)

# Save the map
map_.save("co2_flux_comparison_map.html")# Function to safely get API response and handle errors
def get_api_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print(f"URL: {url}")
        print(f"Response content: {response.text}")
        return None

# 2020
co2_flux_1_url = (
    f"{RASTER_API_URL}/collections/{items[list(items.keys())[0]]['collection']}/items/{items[list(items.keys())[0]]['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}"
)
co2_flux_1 = get_api_response(co2_flux_1_url)

# 2019
co2_flux_2_url = (
    f"{RASTER_API_URL}/collections/{items[list(items.keys())[1]]['collection']}/items/{items[list(items.keys())[1]]['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}"
)
co2_flux_2 = get_api_response(co2_flux_2_url)

# Print API response information for debugging
print("API Response for 2020:")
print(json.dumps(co2_flux_1, indent=2))
print("\nAPI Response for 2019:")
print(json.dumps(co2_flux_2, indent=2))

# Check if 'tiles' key exists before accessing it
if co2_flux_1 and 'tiles' in co2_flux_1:
    print("2020 Tile URL:", co2_flux_1["tiles"][0])
else:
    print("Error: 'tiles' key not found in 2020 data")

if co2_flux_2 and 'tiles' in co2_flux_2:
    print("2019 Tile URL:", co2_flux_2["tiles"][0])
else:
    print("Error: 'tiles' key not found in 2019 data")

# Set the initial zoom level and center of map for both tiles
map_ = folium.plugins.DualMap(location=(34, -118), zoom_start=6)

# For 2020 data
if co2_flux_1 and 'tiles' in co2_flux_1:
    folium.TileLayer(
        tiles=co2_flux_1["tiles"][0],
        attr="GHG Center 2020",
        name="CO2 Flux 2020",
        overlay=True,
        control=True,
        opacity=0.7,
    ).add_to(map_.m1)

# For 2019 data
if co2_flux_2 and 'tiles' in co2_flux_2:
    folium.TileLayer(
        tiles=co2_flux_2["tiles"][0],
        attr="GHG Center 2019",
        name="CO2 Flux 2019",
        overlay=True,
        control=True,
        opacity=0.7,
    ).add_to(map_.m2)

# Add layer controls
folium.LayerControl().add_to(map_.m1)
folium.LayerControl().add_to(map_.m2)

# Add colormap
colormap = plt.cm.get_cmap(color_map)
colors = [matplotlib.colors.rgb2hex(colormap(i)[:3]) for i in range(colormap.N)]

colormap = folium.LinearColormap(
    colors=colors,
    vmin=rescale_values['min'],
    vmax=rescale_values['max'],
    caption='CO2 Flux (g C m-2 day-1)'
)
colormap.add_to(map_.m1)
colormap.add_to(map_.m2)

# Save the map
map_.save("co2_flux_comparison_map.html")