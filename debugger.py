import pandas as pd
import requests

# API URL
url = "https://api.footprintnetwork.org/v1/data/100/all/EFCtot"

# Your API credentials
user_name = 'any-user-name'  # Replace with your actual username
api_key = '1Veijtr0qGNr1j1Rl7M7Vs3roa6V420H1Fcv9b43tD0E0G74u9dc'  # Your provided API key

# Set up headers for the request
headers = {
    "Accept": "application/json"  # This specifies that we want a JSON response
}

# Fetch data from the API
try:
    response = requests.get(url, auth=(user_name, api_key), headers=headers)

    # Debugging the response
    if response.status_code == 200:
        api_data = response.json()
        df_api = pd.DataFrame(api_data)
        print("API DataFrame created successfully:")
        print(df_api.head())
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        df_api = pd.DataFrame()  # Set df_api to empty DataFrame if fetch fails

except requests.exceptions.RequestException as e:
    print(f"An error occurred while making the request: {e}")
    df_api = pd.DataFrame()  # Set df_api to empty DataFrame if an exception occurs

# Optional: Check if the DataFrame is empty
if df_api.empty:
    print("No data retrieved from the API.")
