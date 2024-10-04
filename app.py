import folium
import webbrowser
import os

def create_map():
    # Create a map centered on the world
    m = folium.Map(location=[0, 0], zoom_start=2)
    
    # Save the initial map
    m.save("world_map.html")
    
    # Open the map in the default web browser
    webbrowser.open('file://' + os.path.realpath("world_map.html"))
    
    markers = []
    
    while True:
        user_input = input("Enter latitude and longitude (comma-separated) or 'done' to finish: ")
        
        if user_input.lower() == 'done':
            break
        
        try:
            lat, lon = map(float, user_input.split(','))
            folium.Marker([lat, lon]).add_to(m)
            markers.append((lat, lon))
            print(f"Marker added at: Lat {lat}, Lon {lon}")
            
            # Save and refresh the map
            m.save("world_map.html")
            print("Map updated. Please refresh your browser to see the new marker.")
        except ValueError:
            print("Invalid input. Please enter latitude and longitude as numbers separated by a comma.")
    
    return markers

if __name__ == "__main__":
    print("A world map will open in your browser.")
    print("You can then enter coordinates in the console to add markers.")
    markers = create_map()
    
    print("\nAll marker coordinates:")
    for i, (lat, lon) in enumerate(markers, 1):
        print(f"Marker {i}: Lat {lat}, Lon {lon}")