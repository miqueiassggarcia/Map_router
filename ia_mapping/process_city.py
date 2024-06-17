import json

# Read GeoJSON file
with open('map_data/patos.geojson') as f:
  data = json.load(f)

def calculate_distance(coordinates1, coordinates2):
  # Euclidean distance calculation
  return ((coordinates1[0] - coordinates2[0]) ** 2 + 
    (coordinates1[1] - coordinates2[1]) ** 2) ** 0.5

# Extract nodes and their coordinates
graph = {}
for feature in data['features']:
  coords = feature['geometry']['coordinates']
  if(feature["properties"]["@id"][0] == "n"):
    continue
  for i in range(len(coords)):
    node = tuple(coords[i])
    if(node not in graph):
      graph[node] = []

    if("oneway" not in feature["properties"] or feature["properties"]["oneway"] == "no"):
      if(i > 0):
        node0 = tuple(coords[i-1])
        distance = calculate_distance(node, node0)
        if(node0 not in graph[node]):
          graph[node].append(node0)
          # graph[node].append({
          #   "connect_to": node0,
          #   "distance": distance*6371,
          # })
    if(i < len(coords) - 1):
      node1 = tuple(coords[i+1])
      distance = calculate_distance(node, node1)
      if(node1 not in graph[node]):
        graph[node].append(node1)
        # graph[node].append({
        #   "connect_to": node1,
        #   "distance": distance*6371,
        # })

# print(graph)