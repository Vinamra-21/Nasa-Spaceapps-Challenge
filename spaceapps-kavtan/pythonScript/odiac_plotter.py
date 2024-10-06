import requests
import folium
from folium import Map
import pandas as pd
import matplotlib.pyplot as plt

# STAC and RASTER API URLs
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# Collection name for ODIAC dataset
collection_name = "odiac-ffco2-monthgrid-v2023"
asset_name = "co2-emissions"

# Texas AOI polygon definition
texas_aoi = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "coordinates": [
            [
                [-104, 29],  # SW
                [-104, 33],  # NW
                [-95, 33],   # NE
                [-95, 29],   # SE
                [-104, 29]   # Closing polygon
            ]
        ],
        "type": "Polygon",
    },
}

# Create a map to display the polygon
aoi_map = Map(
    tiles="OpenStreetMap",
    location=[30, -100],
    zoom_start=6,
)

# Add the polygon to the map
folium.GeoJson(texas_aoi, name="Texas, USA").add_to(aoi_map)
aoi_map.save("texas_aoi_map.html")

# Fetch items from the STAC API
try:
    response = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit=300")
    response.raise_for_status()  # Raise an error for bad responses
    items = response.json()["features"]
    print(f"Found {len(items)} items")
except requests.exceptions.RequestException as e:
    print(f"Error fetching items: {e}")
    items = []

# Function to generate statistics for a specific granule
def generate_stats(item, geojson):
    if asset_name not in item["assets"]:
        print(f"Asset {asset_name} not found in item {item['id']}")
        return {}

    try:
        result = requests.post(
            f"{RASTER_API_URL}/cog/statistics",
            params={"url": item["assets"][asset_name]["href"]},
            json=geojson,
        )
        result.raise_for_status()  # Raise an error for bad responses

        # Return the statistics and datetime information
        return {
            **result.json()["properties"],
            "start_datetime": item["properties"]["start_datetime"][:7],
        }
    except requests.exceptions.RequestException as e:
        print(f"Error generating statistics for item {item['id']}: {e}")
        return {}

# Generate statistics for all items
stats = [generate_stats(item, texas_aoi) for item in items if item]
if stats:
    print(stats[0])
else:
    print("No statistics generated.")
