import requests
import pandas as pd
import matplotlib.pyplot as plt
import finder

# API URLs
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# Collection name for CO₂ Budgets dataset 
COLLECTION_NAME = "oco2-mip-co2budget-yeargrid-v1"
ASSET_NAME = "ff"

# Fetch items from the STAC API collection
def fetch_collection_items(collection_name, limit=600):
    response = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={limit}")
    return response.json()["features"]

# Generate statistics for a given item and GeoJSON polygon
def generate_stats(item, geojson):
    response = requests.post(
        f"{RASTER_API_URL}/cog/statistics",
        params={"url": item["assets"][ASSET_NAME]["href"]},
        json=geojson,
    )
    return {
        **response.json()["properties"],
        "datetime": item["properties"]["start_datetime"],
    }

# Clean JSON stats data and convert it to a DataFrame
def clean_stats(stats):
    df = pd.json_normalize(stats)
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]
    df["datetime"] = pd.to_datetime(df["datetime"])
    
    # Filter out data from 2020 or rows with max values equal to 0
    df = df[(df["datetime"].dt.year != 2020) & (df["max"] != 0)]
    
    return df

# Create an area of interest (AOI) polygon for the specified location
def create_aoi_polygon(latitude, longitude, offset=0.1):
    lat1, lat2, lon1, lon2 = latitude - offset, latitude + offset, longitude - offset, longitude + offset
    return {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [lat1, lon1],
                [lat1, lon2],
                [lat2, lon2],
                [lat2, lon1],
                [lat1, lon1]
            ]]
        },
    }

# Plot the CO2 emission data
def plot_co2_emission(df, location_name):
    plt.figure(figsize=(20, 10))
    plt.plot(df["datetime"], df["max"], color="red", linestyle="-", linewidth=0.5, label="CO2 emissions")
    plt.legend()
    plt.xlabel("Years")
    plt.ylabel("CO2 emissions (gC/m²/year)")
    plt.title(f"CO2 Emission Values for {location_name} (Filtered Data)")
    plt.text(df["datetime"].iloc[0], df["max"].min(), "Source: NASA/NOAA OCO-2 MIP Top-Down CO₂ Budgets", fontsize=12, color="blue")
    plt.savefig('E:/Web Development/Projects-IIT/Nasa-Spaceapps-Challenge/spaceapps-kavtan/public/map.png')

# Generate CO2 emission graph for a given location
def generate_co2_emission_graph(location_name):
    latitude, longitude = finder.latlongfind(location_name)
    aoi = create_aoi_polygon(latitude, longitude)
    items = fetch_collection_items(COLLECTION_NAME)
    stats = [generate_stats(item, aoi) for item in items]
    df = clean_stats(stats)
    if not df.empty:
        plot_co2_emission(df, location_name)
    else:
        print(f"No valid data found for {location_name} after filtering.")

# Main function
def main():
    location_name = input("Enter location name: ")
    generate_co2_emission_graph(location_name)

if __name__ == "__main__":
    main()
