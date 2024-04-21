import json
import time
import random

from dijkstra import dijkstra, calculate_distance
from process import graph, data

start_time = time.time()

initial = (-37.2668079, -7.0136892)
start = (-37.2668079, -7.0136892)
points = []

for i in range(20):
  random_int = random.randint(0, len(data["features"]))
  way = data["features"][random_int]["geometry"]["coordinates"]
  point = way[random.randint(0, len(way) - 1)]
  points.append(tuple(point))

def neartest_point(start, points):
  current_end = [(float('inf'), float('inf')), (float('inf')), 0]
  for i in range(len(points)):
    (distance) = calculate_distance(start, points[i])
    if(distance < current_end[1]):
      current_end[0] = points[i]
      current_end[1] = distance
      current_end[2] = i
  
  return current_end[0], current_end[2]

sequence = [start]
nodes = []
while len(points) > 0:
  end, index = neartest_point(start, points)
  points.pop(index)
  sequence.append(end)

  if start in graph and end in graph:
      path, distance = dijkstra(graph, start, end)
      if path is not None:
        if(start != initial):
          path.pop(0)
        nodes += [list(coordinates) for coordinates in path]
      else:
          print("No path found between the" + str(start) + " and end" + str(end) + " nodes.")
  else:
      print("Start or end node is not in the graph.")

  start = end


output = {
  "type": "FeatureCollection",
  "generator": "overpass-turbo",
  "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.",
  "sequence": sequence,
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": nodes
      }
    }
  ]
}

json_output = json.dumps(output, indent=4)

with open("../web/output.geojson", "w") as json_file:
  json_file.write(json_output)

end_time = time.time()

execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")