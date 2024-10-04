# Randi code, dont use this shit. 

import finder
import requests
import pandas as pd
import matplotlib.pyplot as plt

# The STAC API is a catalog of all the existing data collections that are stored in the GHG Center.
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"

# The RASTER API is used to fetch collections for visualization
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# The collection name is used to fetch the dataset from the STAC API. First, we define the collection name as a variable
# Name of the collection for CEOS National Top-Down CO₂ Budgets dataset 
collection_name = "oco2-mip-co2budget-yeargrid-v1"

# Fetch the collection from the STAC API using the appropriate endpoint
# The 'requests' library allows a HTTP request possible
collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()

asset_name = 'ff'

def generate_stats(item, geojson):

    # A POST request is made to submit the data associated with the item of interest (specific observation) within the boundaries of the polygon to compute its statistics
    result = requests.post(

        # Raster API Endpoint for computing statistics
        f"{RASTER_API_URL}/cog/statistics",

        # Pass the URL to the item, asset name, and raster identifier as parameters
        params={"url": item["assets"][asset_name]["href"]},

        # Send the GeoJSON object (polygon) along with the request
        json=geojson,

    # Return the response in JSON format
    ).json()

    # Return a dictionary containing the computed statistics along with the item's datetime information.
    return {
        **result["properties"],
        "datetime": item["properties"]["start_datetime"],
    }

def clean_stats(stats_json) -> pd.DataFrame:

    # Normalize the JSON data
    df = pd.json_normalize(stats_json)

    # Replace the naming "statistics.b1" in the columns
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]

    # Set the datetime format
    df["date"] = pd.to_datetime(df["datetime"])

    # Return the cleaned format
    return df

def make_co2_emission_graph_please(loc_name):
    latitude, longitude = finder.latlongfind(loc_name)

    lat1, lat2, lon1, lon2 = finder.calculate_coordinates(latitude, longitude)

    # Create a polygon for the area of interest (aoi)
    aoi = {
        "type": "Feature", # Create a feature object
        "properties": {},
        "geometry": { # Set the bounding coordinates for the polygon
            "coordinates": [
                [
                    [lat1, lon1], # South-east bounding coordinate
                    [lat1, lon2], # North-east bounding coordinate
                    [lat2, lon1], # North-west bounding coordinate
                    [lat2, lon2], # South-west bounding coordinate
                    [lat1, lon1]  # South-east bounding coordinate (closing the polygon)
                ]
            ],
            "type": "Polygon",
        },
    }

    # Check total number of items available within the collection
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit=600").json()["features"]

    # Print the total number of items (granules) found
    print(f"Found {len(items)} items")
        # Now we create a dictionary where the start datetime values for each granule is queried more explicitly by year and month (e.g., 2020-02)
    items = {item["properties"]["start_datetime"]: item for item in items} 

    # Next, we need to specify the asset name for this collection
    # The asset name is referring to the raster band containing the pixel values for the parameter of interest
    # For the case of the OCO-2 MIP Top-Down CO₂ Budgets collection, the parameter of interest is “ff”
    asset_name = "ff" #fossil fuel

    # Fetching the min and max values for a specific item
    rescale_values = {"max":items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"], "min":items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]}

    # Hardcoding the min and max values to match the scale in the GHG Center dashboard
    rescale_values = {"max": 450, "min": 0}

    color_map = "purd"

    co2_flux_1 = requests.get(

        # Pass the collection name, the item number in the list, and its ID
        f"{RASTER_API_URL}/collections/{items[list(items.keys())[0]]['collection']}/items/{items[list(items.keys())[0]]['id']}/tilejson.json?"

        # Pass the asset name
        f"&assets={asset_name}"

        # Pass the color formula and colormap for custom visualization
        f"&color_formula=gamma+r+1.05&colormap_name={color_map}"

        # Pass the minimum and maximum values for rescaling
        f"&rescale={rescale_values['min']},{rescale_values['max']}", 

    # Return the response in JSON format
    ).json()

    # Check total number of items available within the collection
    items = requests.get(
        f"{STAC_API_URL}/collections/{collection_name}/items?limit=600"
    ).json()["features"]

    # Print the total number of items (granules) found
    print(f"Found {len(items)} items")

    # Generate a for loop that iterates over all the existing items in the collection
    for item in items:

        # The loop will then retrieve the information for the start datetime of each item in the list
        print(item["properties"]["start_datetime"])

        # Exit the loop after printing the start datetime for the first item in the collection
        break

    # Generate statistics using the created function "generate_stats" within the bounding box defined by the polygon
    stats = [generate_stats(item, aoi) for item in items]

    # Apply the generated function on the stats data
    df = clean_stats(stats)

    # Figure size: 20 representing the width, 10 representing the height
    fig = plt.figure(figsize=(20, 10))

    plt.plot(
        df["datetime"], # X-axis: sorted datetime
        df["max"], # Y-axis: maximum CO₂ emission
        color="red", # Line color
        linestyle="-", # Line style
        linewidth=0.5, # Line width
        label="CO2 emissions", # Legend label
    )

    # Display legend
    plt.legend()

    # Insert label for the X-axis
    plt.xlabel("Years")

    # Insert label for the Y-axis
    plt.ylabel("CO2 emissions gC/m2/year1")

    # Insert title for the plot
    plt.title(f"CO2 emission Values for {loc_name} (2015-2020)")

    # Add data citation
    plt.text(
        df["datetime"].iloc[0],           # X-coordinate of the text 
        df["max"].min(),                  # Y-coordinate of the text 


        # Text to be displayed
        "Source: NASA/NOAA OCO-2 MIP Top-Down CO₂ Budgets",                  
        fontsize=12,                             # Font size
        horizontalalignment="left",              # Horizontal alignment
        verticalalignment="top",                 # Vertical alignment
        color="blue",                            # Text color
    )

    # Plot the time series
    plt.show()


def main():
    loc = input("Enter location name: ")
    make_co2_emission_graph_please(loc)

if __name__ == "__main__":
    main()
