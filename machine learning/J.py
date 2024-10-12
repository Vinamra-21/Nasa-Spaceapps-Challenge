import requests
import pandas as pd
import matplotlib.pyplot as plt

# STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name = "odiac-ffco2-monthgrid-v2023"

# Function to get item count in a collection
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

# Apply the function to the data collection
number_of_items = get_item_count(collection_name)
items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]

# Extract items into a dictionary by start datetime
items_dict = {item["properties"]["start_datetime"][:7]: item for item in items} 
asset_name = "co2-emissions"

# Fetch rescale values for the first item
rescale_values = {
    "max": items_dict[list(items_dict.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
    "min": items_dict[list(items_dict.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
}

# Define area of interest for Texas
texas_aoi = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-95, 29],
                    [-95, 33],
                    [-104, 33],
                    [-104, 29],
                    [-95, 29]
                ]],
            },
            "properties": {}
        }
    ]
}

# Function to generate statistics for items in the defined area
def generate_stats(item, geojson):
    result = requests.post(
        f"{RASTER_API_URL}/cog/statistics",
        params={"url": item["assets"][asset_name]["href"]},
        json=geojson,
    ).json()

    # Check if the result contains 'features' and access the first feature
    if "features" not in result or len(result["features"]) == 0:
        print(f"Error: 'features' key not found or empty in response for item {item['id']}")
        print(f"Response: {result}")  # Print the response for debugging
        return None  # Return None or handle as needed
    
    properties = result["features"][0]["properties"]
    
    # Access the data you need for graphing
    stats_data = properties["statistics"]["b1"]

    return {
        "min": stats_data["min"],
        "max": stats_data["max"],
        "mean": stats_data["mean"],
        "std": stats_data["std"],
        "median": stats_data["median"],
        "valid_percent": stats_data["valid_percent"],
        "count": stats_data["count"],
        "start_datetime": item["properties"]["start_datetime"][:7],
    }
# Generate statistics and filter out None results
stats = [generate_stats(item, texas_aoi) for item in items]
stats = [s for s in stats if s is not None]  # Remove None results


# Generate statistics for all items
stats = [generate_stats(item, texas_aoi) for item in items]

# Convert statistics to DataFrame
def clean_stats(stats_json) -> pd.DataFrame:
    df = pd.json_normalize(stats_json)
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]
    df["date"] = pd.to_datetime(df["start_datetime"])
    return df

df = clean_stats(stats)

# Plotting the results
plt.figure(figsize=(20, 10))
plt.plot(df["date"], df["max"], color="red", linewidth=0.5, label="Max monthly CO₂ emissions")
plt.legend()
plt.xlabel("Years")
plt.ylabel("CO2 emissions gC/m²/d")
plt.title("CO2 Emission Values for Texas, Dallas (2000-2022)")
plt.text(df["date"].iloc[0], df["max"].min(), "Source: NASA ODIAC Fossil Fuel CO₂ Emissions", fontsize=12, color="blue")
plt.show()
