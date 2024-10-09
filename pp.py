import requests
import folium
import folium.plugins
import pandas as pd
import matplotlib.pyplot as plt
import math
import time

# STAC and RASTER API endpoints
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name = "sedac-popdensity-yeargrid5yr-v4.11"

def get_coordinates(location_name):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "YourAppName/1.0"  # Replace with your app name
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  
        data = response.json()

        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        else:
            print(f"No results found for '{location_name}'")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def latlongfind(loc_name):
    coordinates = get_coordinates(loc_name)
    if coordinates:
        latitude, longitude = coordinates
        return latitude, longitude

def calculate_coordinates(lat, lon):
    R = 6371  
    d = 30  

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    angular_distance = d / R

    north_lat = math.degrees(math.asin(
        math.sin(lat_rad) * math.cos(angular_distance) +
        math.cos(lat_rad) * math.sin(angular_distance)
    ))
    
    south_lat = math.degrees(math.asin(
        math.sin(lat_rad) * math.cos(angular_distance) - 
        math.cos(lat_rad) * math.sin(angular_distance)
    ))
    
    if abs(lat) > 89.9:
        east_lon = lon + 180
        west_lon = lon - 180
    else:
        delta_lon = math.atan2(
            math.sin(angular_distance) * math.cos(lat_rad),
            math.cos(angular_distance) - math.sin(lat_rad) * math.sin(lat_rad)
        )
        east_lon = math.degrees(lon_rad + delta_lon)
        west_lon = math.degrees(lon_rad - delta_lon)

    east_lon = (east_lon + 180) % 360 - 180
    west_lon = (west_lon + 180) % 360 - 180

    return north_lat, south_lat, east_lon, west_lon

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

def main(location_name):
    # Fetch coordinates for the given location
    coordinates = latlongfind(location_name)
    if coordinates:
        latitude, longitude = coordinates
        print(f"Coordinates for {location_name}: Latitude: {latitude}, Longitude: {longitude}")
        
        # Define Area of Interest (AOI) based on coordinates
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

        # Get item count and items from STAC API
        number_of_items = get_item_count(collection_name)
        items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]
        
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

        # Fetch tiles for January 2020 and January 2000
        january_2020_tile = requests.get(
            f"{RASTER_API_URL}/collections/{items['2020-01']['collection']}/items/{items['2020-01']['id']}/tilejson.json?"
            f"&assets={asset_name}&color_formula=gamma+r+1.05&colormap_name={color_map}"
            f"&rescale={rescale_values['min']},{rescale_values['max']}").json()

        january_2000_tile = requests.get(
            f"{RASTER_API_URL}/collections/{items['2000-01']['collection']}/items/{items['2000-01']['id']}/tilejson.json?"
            f"&assets={asset_name}&color_formula=gamma+r+1.05&colormap_name={color_map}"
            f"&rescale={rescale_values['min']},{rescale_values['max']}").json()

        if "tiles" not in january_2020_tile or "tiles" not in january_2000_tile:
            print("Error: Tiles not found in the response for one of the years.")
            return
        
        # Set up dual map for visualization
        map_ = folium.plugins.DualMap(location=(latitude, longitude), zoom_start=6)
        folium.TileLayer(tiles=january_2020_tile["tiles"][0], attr="GHG", opacity=1).add_to(map_.m1)
        folium.TileLayer(tiles=january_2000_tile["tiles"][0], attr="GHG", opacity=1).add_to(map_.m2)

        # Save the dual map
        map_.save("dual_map.html")
        print("Dual map saved as 'dual_map.html'.")

        # Fetch items again to check total number
        items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit=300").json()["features"]
        print(f"Found {len(items)} items")

        # Generate statistics for Texas AOI
        def generate_stats(item, geojson):
            result = requests.post(
                f"{RASTER_API_URL}/cog/statistics",
                params={"url": item["assets"][asset_name]["href"]},
                json=geojson,
            ).json()
            return {**result["properties"], "start_datetime": item["properties"]["start_datetime"]}

        stats = [generate_stats(item, texas_aoi) for item in items]

        # Clean statistics into DataFrame
        def clean_stats(stats_json) -> pd.DataFrame:
            df = pd.json_normalize(stats_json)
            df.columns = [col.replace("statistics.b1.", "") for col in df.columns]
            df["date"] = pd.to_datetime(df["start_datetime"])
            return df

        df = clean_stats(stats)
        print(df.head(5))

        # Plotting the population density over the years
        fig = plt.figure(figsize=(20, 10))
        plt.plot(df["date"], df["max"], color="red", linestyle="-", linewidth=0.5, label="Population density over the years")
        plt.legend()
        plt.xlabel("Years")
        plt.ylabel("Population Density")
        plt.title(f"Population Density over {location_name} (2000-2020)")

        # Add data citation
        plt.text(
            df["date"].iloc[0], 
            df["max"].max(), 
            "Source: SEDAC Population Density Dataset", 
            fontsize=12, 
            ha='center'
        )
        plt.show()

if __name__ == "__main__":
    location_name = "Texas, USA"  # You can change this to any other location
    main(location_name)
