import requests
import csv

# STAC API endpoint
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
collection_name = "gosat-based-ch4budget-yeargrid-v1"

# Fetch the collection
collection_url = f"{STAC_API_URL}/collections/{collection_name}/items"
response = requests.get(collection_url)

if response.ok:
    collection = response.json()
    items = collection.get("features", [])
    
    if items:
        # Create and open a CSV file
        with open("methane_data.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            
            # Write header to the CSV
            header = ["id", "datetime", "geometry", "properties"]
            writer.writerow(header)
            
            # Loop through items and extract relevant data
            for item in items:
                item_id = item.get("id", "")
                datetime = item.get("properties", {}).get("datetime", "")
                geometry = item.get("geometry", "")
                properties = item.get("properties", "")
                
                # Write row to the CSV
                writer.writerow([item_id, datetime, geometry, properties])
        
        print("Data written to methane_data.csv")
    else:
        print("No items found in the collection.")
else:
    print("Error fetching the collection.")
