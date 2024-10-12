# Install the Required Libraries
# Ensure the required libraries are installed
# %pip install requests folium rasterstats pystac_client pandas matplotlib --quiet

# Import the following libraries
import requests
import folium
import folium.plugins
from folium import Map, TileLayer
from pystac_client import Client
import pandas as pd
import matplotlib.pyplot as plt

# Provide the STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# The name of the collection for MiCASA Land Carbon Flux
collection_name = "micasa-carbonflux-daygrid-v1"
asset_name = "rh"  # Heterotrophic Respiration

def fetch_collection(collection_name):
    """Fetch the collection from the STAC API."""
    collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()
    print("Fetched collection properties.")
    return collection

def get_item_count(collection_id):
    """Get the count of items (granules) in the collection."""
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"
    
    while True:
        response = requests.get(items_url)
        if not response.ok:
            print("Error getting items.")
            return count

        stac = response.json()
        count += int(stac["context"].get("returned", 0))
        next_link = [link for link in stac["links"] if link["rel"] == "next"]
        if not next_link:
            break
        items_url = next_link[0]["href"]

    print(f"Total items found: {count}")
    return count

def get_items(collection_name):
    """Retrieve items from the collection."""
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit=800").json()["features"]
    print(f"Found {len(items)} items.")
    return items

def fetch_raster_data(date, items, asset_name):
    """Fetch raster data for a given date."""
    tile_data = requests.get(
        f"{RASTER_API_URL}/collections/{items[date]['collection']}/items/{items[date]['id']}/tilejson.json?"
        f"&assets={asset_name}&color_formula=gamma+r+1.05"
    ).json()
    
    print(f"Fetched raster data for {date}.")
    return tile_data

def plot_rh_values(dates, rh_values):
    """Plot the RH values over time."""
    plt.figure(figsize=(20, 10))
    plt.plot(dates, rh_values, color="purple", linestyle="-", linewidth=0.5, label="RH Level")
    plt.xlabel("Date")
    plt.ylabel("gm Carbon/m²/day")
    plt.title("Heterotrophic Respiration Values Over Time")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main input-output system
def run_micasa_analysis(start_date='2023-01-01', end_date='2023-01-31'):
    """Run the MiCASA Land Carbon Flux analysis."""
    
    print("Starting MiCASA Land Carbon Flux analysis...")
    
    # Step 1: Fetch collection
    collection = fetch_collection(collection_name)
    
    # Step 2: Get item count
    item_count = get_item_count(collection_name)
    
    # Step 3: Get items
    items = get_items(collection_name)
    
    # Step 4: Get min and max values for rescaling
    items = {item["properties"]["datetime"][:10]: item for item in items}
    rescale_values = {
        "max": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
        "min": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
    }

    # Step 5: Fetch raster data for the two dates
    rh_values = []
    dates = []
    
    for date in [start_date, end_date]:
        tile_data = fetch_raster_data(date, items, asset_name)
        rh_value = tile_data["assets"][asset_name]["href"]  # Use the appropriate value for RH
        rh_values.append(rh_value)  # Replace with actual RH value extraction logic
        dates.append(date)

    # Step 6: Plot the RH values
    plot_rh_values(dates, rh_values)

# Example of running the analysis
run_micasa_analysis('2023-01-01', '2023-01-02')
