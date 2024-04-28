import requests

# Step 1: Get coordinates for the postcode
postcode = "58700350"
geocoding_url = f"https://nominatim.openstreetmap.org/search?postalcode={postcode}&format=json"
response = requests.get(geocoding_url)
data = response.json()
if data:
    latitude = data[0]['lat']
    longitude = data[0]['lon']
else:
    print("No results found for the postcode.")
    exit()

# Step 2: Perform reverse geocoding lookup to get ways
overpass_url = "http://overpass-api.de/api/interpreter"
query = f"""
    [out:json];
    way(around:1000,{latitude},{longitude});
    out;
"""
response = requests.get(overpass_url, params={'data': query})
ways_data = response.json()

# Step 3: Extract relevant way data
if 'elements' in ways_data:
    ways = [element for element in ways_data['elements'] if element['type'] == 'way']
    for way in ways:
        print(way)  # Print or process the way data as needed
else:
    print("No ways found for the given coordinates.")
