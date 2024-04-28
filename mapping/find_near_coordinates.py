import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def find_nearby_coordinates(center_coords, coordinates_list, radius):
    nearby_coordinates = []
    for coord in coordinates_list:
        if haversine(center_coords[0], center_coords[1], coord[0], coord[1]) <= radius:
            nearby_coordinates.append(coord)
    return nearby_coordinates