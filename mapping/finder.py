import json
import time

from dijkstra import dijkstra
from process import graph, data
from generate_points import generate_random_points
from get_next_optimal_point import neartest_point

start_time = time.time()

initial = (-37.2668079, -7.0136892)
start = (-37.2668079, -7.0136892)
points = []

generate_random_points(points, data)

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