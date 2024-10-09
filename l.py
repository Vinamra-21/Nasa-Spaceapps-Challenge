import requests
import pandas as pd
import matplotlib.pyplot as plt
import math

# STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
COLLECTION_NAME = "sedac-popdensity-yeargrid5yr-v4.11"

def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_item_count(collection_id):
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"

    while True:
        stac = fetch_json(items_url)
        count += int(stac["context"].get("returned", 0))
        next_url = [link for link in stac["links"] if link["rel"] == "next"]

        if not next_url:
            break
        items_url = next_url[0]["href"]

    return count

def fetch_items(collection_name):
    number_of_items = get_item_count(collection_name)
    items_url = f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}"
    return fetch_json(items_url)["features"]

def get_rescale_values(items, asset_name):
    first_item = items[list(items.keys())[0]]
    return {
        "max": first_item["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
        "min": first_item["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
    }

def get_coordinates(location_name):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "YourAppName/1.0"}

    response = requests.get(base_url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    else:
        print(f"No results found for '{location_name}'")
        return None

def calculate_coordinates(lat, lon, distance_km=15):
    R = 6371  
    angular_distance = distance_km / R

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    north_lat = math.degrees(math.asin(math.sin(lat_rad) * math.cos(angular_distance) +
                                        math.cos(lat_rad) * math.sin(angular_distance)))
    south_lat = math.degrees(math.asin(math.sin(lat_rad) * math.cos(angular_distance) - 
                                        math.cos(lat_rad) * math.sin(angular_distance)))

    delta_lon = math.atan2(
        math.sin(angular_distance) * math.cos(lat_rad),
        math.cos(angular_distance) - math.sin(lat_rad) * math.sin(lat_rad)
    )
    
    east_lon = math.degrees(lon_rad + delta_lon)
    west_lon = math.degrees(lon_rad - delta_lon)

    return north_lat, south_lat, east_lon, west_lon

def create_aoi_polygon(latitude, longitude):
    lat1, lat2, lon1, lon2 = calculate_coordinates(latitude, longitude)
    return {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "coordinates": [[
                [lon1, lat1],
                [lon2, lat1],
                [lon2, lat2],
                [lon1, lat2],
                [lon1, lat1]
            ]],
            "type": "Polygon",
        },
    }

def generate_stats(item, geojson, asset_name):
    if "assets" in item and asset_name in item["assets"]:
        result = requests.post(
            f"{RASTER_API_URL}/cog/statistics",
            params={"url": item["assets"][asset_name]["href"]},
            json=geojson,
        ).json()
        return {**result["properties"], "start_datetime": item["properties"]["start_datetime"]}
    else:
        print(f"Missing assets for item with id: {item.get('id')}")
        return {}

def clean_stats(stats_json) -> pd.DataFrame:
    df = pd.json_normalize(stats_json)
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]
    df["date"] = pd.to_datetime(df["start_datetime"])
    return df

# Main execution flow
items = fetch_items(COLLECTION_NAME)
print(f"Found {len(items)} items")

# Create Area of Interest (AOI)
location = 'texas'
latitude, longitude = get_coordinates(location)
aoi = create_aoi_polygon(latitude, longitude)

# Generate statistics for Texas AOI
stats = [generate_stats(item, aoi, "population-density") for item in items]
stats = [stat for stat in stats if stat]  # Filtering out empty results

# Clean stats and display first 5 rows
df = clean_stats(stats)
print(df.head(5))

# Plotting the population density over the years
plt.figure(figsize=(20, 10))
plt.plot(df["date"], df["max"], color="red", linestyle="-", linewidth=0.5, label="Population density over the years")
plt.legend()
plt.xlabel("Years")
plt.ylabel("Population Density")
plt.title("Population Density over Texas (2000-2020)")
plt.text(df["date"].iloc[0], df["max"].max(), "Source: SEDAC Population Density Dataset", fontsize=12, ha='center')
plt.show()
