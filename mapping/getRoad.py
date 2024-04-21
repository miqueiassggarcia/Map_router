import json

# Read GeoJSON file
with open('data/patos.geojson') as f:
  data = json.load(f)

# Extract nodes and their coordinates
Roads = []
for feature in data['features']:
  if('name' in feature['properties']):
    name = feature['properties']['name']
    if("Rua Godofredo Medeiros" in name):
      Roads.append({
        "type": feature["type"],
        "properties": {
          "@id": feature['properties']['@id'],
          "name": name,
          "highway": feature['properties']['highway']
        },
        "geometry": {
          "type": feature["geometry"]["type"],
          "coordinates": feature['geometry']['coordinates']
        }
      })

path = []
for road in Roads:
  path.extend(road['geometry']['coordinates'])

print(path[round(len(path) / 2)-1])