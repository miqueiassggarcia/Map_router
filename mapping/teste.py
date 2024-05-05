import requests

# Step 1: Get coordinates for the city
city_name = "Patos"
geocoding_url = f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json"
response = requests.get(geocoding_url)
data = response.json()
if data:
    city_latitude = data[0]['lat']
    city_longitude = data[0]['lon']
else:
    print("No results found for the city.")
    exit()

# Step 2: Perform reverse geocoding lookup to get objects within the city
overpass_url = "http://overpass-api.de/api/interpreter"
query = f"""
    [out:json];
    (
        node["addr:postcode"](around:10000,{city_latitude},{city_longitude});
        way["addr:postcode"](around:10000,{city_latitude},{city_longitude});
        relation["addr:postcode"](around:10000,{city_latitude},{city_longitude});
    );
    out;
"""
response = requests.get(overpass_url, params={'data': query})
city_objects_data = response.json()

# Step 3: Extract postcodes from the returned objects
postcodes = set()
for element in city_objects_data['elements']:
    if 'tags' in element and 'addr:postcode' in element['tags']:
        postcodes.add(element['tags']['addr:postcode'])

# Print or process the postcodes as needed
for postcode in postcodes:
    print(postcode)