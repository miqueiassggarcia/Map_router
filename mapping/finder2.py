from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
import json

# Load the GeoJSON data
with open('patos.geojson') as f:
    data = json.load(f)

# Define the coordinate you want to find the nearest way to
target_point = Point(-37.2900, -7.0300)  # Example coordinate

# Initialize variables to store nearest way, its ID, and its distance
nearest_way = None
nearest_way_id = None
nearest_distance = float('inf')

# Iterate over features in the GeoJSON data
for feature in data['features']:
    # Extract coordinates and create a LineString geometry
    coordinates = feature['geometry']['coordinates']
    line = LineString(coordinates)
    
    # Find the nearest point on the LineString to the target point
    nearest_point_on_line = nearest_points(line, target_point)[0]
    
    # Calculate distance between target point and nearest point on the line
    distance = target_point.distance(nearest_point_on_line)
    
    # Update nearest way if the distance is smaller
    if distance < nearest_distance:
        nearest_way = line
        nearest_way_id = feature['properties']['@id'] if '@id' in feature['properties'] else None
        nearest_distance = distance

# Print the nearest way, its ID, and its distance
print("Nearest Way ID:", nearest_way_id)
print("Nearest Way:", nearest_way)
print("Distance:", nearest_distance)