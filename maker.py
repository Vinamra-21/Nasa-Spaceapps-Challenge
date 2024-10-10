import pandas as pd
import requests
import time

# Your API credentials
user_name = 'any-user-name'  # Replace with your actual username
api_key = '1Veijtr0qGNr1j1Rl7M7Vs3roa6V420H1Fcv9b43tD0E0G74u9dc'  # Your provided API key

# Set up headers for the request
headers = {
    "Accept": "application/json"  # This specifies that we want a JSON response
}

df = pd.DataFrame()  # Initialize an empty DataFrame to store the data

try:
    for i in range(2, 250):
        url = f"https://api.footprintnetwork.org/v1/data/{i}/all/EFCtot"

        try: 
            response = requests.get(url, auth=(user_name, api_key), headers=headers)

            # Debugging the response
            if response.status_code == 200:
                api_data = response.json()
                df_api = pd.DataFrame(api_data)
                df = pd.concat([df, df_api], ignore_index=True )
                print(f'instance {i} was successful')

            else:
                print(f"Error fetching data: {response.status_code} - {response.text}")
                df.to_csv('trying-data.csv', index=False)
        except:
            print(f'instance {i} failed')
            pass

        time.sleep(1.5)

except requests.exceptions.RequestException as e:
    print(f"An error occurred while making the request: {e}")
    print(len(df))
    df.to_csv('trying-data.csv', index=False)

df.to_csv('imperfect-data.csv', index = False)