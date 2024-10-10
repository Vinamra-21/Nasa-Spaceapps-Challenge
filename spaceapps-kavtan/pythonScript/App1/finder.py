import requests
import time
import math

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
        response.raise_for_status()  # Raise an exception for bad status codes
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
    location_name = loc_name

    coordinates = get_coordinates(location_name)
    if coordinates:
        latitude, longitude = coordinates
        return latitude, longitude
        # print(f"Coordinates for {location_name}:")
        # print(f"Latitude: {latitude}")
        # print(f"Longitude: {longitude}")

def calculate_coordinates(lat, lon):
    # Earth's radius in kilometers
    R = 6371
    
    # Distance to add/subtract (30 km)
    d = 30
    
    # Convert latitude and longitude to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    
    # Angular distance in radians
    angular_distance = d / R
    
    # Calculate new latitudes (North and South)
    north_lat = math.degrees(math.asin(
        math.sin(lat_rad) * math.cos(angular_distance) +
        math.cos(lat_rad) * math.sin(angular_distance)
    ))
    
    south_lat = math.degrees(math.asin(
        math.sin(lat_rad) * math.cos(angular_distance) -
        math.cos(lat_rad) * math.sin(angular_distance)
    ))
    
    # Calculate new longitudes (East and West)
    # We need to handle the special case near the poles
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
    
    # Normalize longitudes to be within -180 to 180
    east_lon = (east_lon + 180) % 360 - 180
    west_lon = (west_lon + 180) % 360 - 180
    
    return north_lat, south_lat, east_lon, west_lon


if __name__ == "__main__":
    while True:   
        latlongfind()  
        time.sleep(1)