import json

# Read GeoJSON file
with open('../map_data/patos.geojson') as f:
  data = json.load(f)

# Extract nodes and their coordinates
graph = {}
for feature in data['features']:
  coords = feature['geometry']['coordinates']
  for i in range(len(coords)):
    node = tuple(coords[i])
    if(node not in graph):
      graph[node] = []

    if("oneway" not in feature["properties"]):
      if(i > 0):
        node0 = tuple(coords[i-1])
        if(node0 not in graph[node]):
          graph[node].append(node0)
    elif(feature["properties"]["oneway"] == "no"):
      if(i > 0):
        node0 = tuple(coords[i-1])
        if(node0 not in graph[node]):
          graph[node].append(node0)

    if(i < len(coords) - 1):
      node1 = tuple(coords[i+1])
      if(node1 not in graph[node]):
        graph[node].append(node1)