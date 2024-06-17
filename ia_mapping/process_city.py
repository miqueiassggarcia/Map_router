import json

# Read GeoJSON file
with open('../map_data/patos/patoscompleto.geojson') as f:
  patoscompleto = json.load(f)
with open('../map_data/patos/patos.geojson') as f:
  patos = json.load(f)
with open('../map_data/patos/patos4.geojson') as f:
  patos4 = json.load(f)
with open('../map_data/patos/patos2.geojson') as f:
  patos2 = json.load(f)
with open('../map_data/patos/patos1.geojson') as f:
  patos1 = json.load(f)

def calculate_distance(coordinates1, coordinates2):
  # Euclidean distance calculation
  return ((coordinates1[0] - coordinates2[0]) ** 2 + 
    (coordinates1[1] - coordinates2[1]) ** 2) ** 0.5

# Extract nodes and their coordinates
def process(data):
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

  return graph

graphpatoscompleto = process(patoscompleto)
graphpatos = process(patos)
graphpatos4 = process(patos4)
graphpatos2 = process(patos2)
graphpatos1 = process(patos1)