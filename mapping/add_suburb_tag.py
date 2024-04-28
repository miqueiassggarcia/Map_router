from shapely.geometry import Point, Polygon
import json
from process import graph

with open('mapping/data/suburbiospatos.geojson') as f:
  data = json.load(f)

# Define your polygon using a list of coordinates
for i in range(len(data['features'])):
  if(data['features'][i]['geometry']["type"] == "Polygon"):
    polygon_coords = data['features'][i]['geometry']['coordinates'][0]
    polygon = Polygon(polygon_coords)
    for key in graph.keys():
      point = Point(key)
      is_inside = point.within(polygon)

      if is_inside:
        graph[key].append(data['features'][i]["properties"]["name"])

nodes = []
for key in graph.keys():
  if(len(graph[key])-1 >= 0):
    if(graph[key][len(graph[key])-1] == "Morro"):
      nodes.append(key)

print("[out:json];\n(")
for node in nodes:
  print("node(around: 1, " + str(node[1]) + ", " + str(node[0]) + ");")
print(");\nout geom;")