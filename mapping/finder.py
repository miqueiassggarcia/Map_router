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

def get_near_point(start, points):
  near = [(float('inf'), float('inf')), (float('inf'))]
  for i in range(len(points)):
    (distance) = calculate_distance(start, points[i])
    if(distance < near[1] and distance != 0):
      near[0] = points[i]
      near[1] = distance
  
  return near

def calculate_distance_of_next(point, points, k=5):
  points_copy = points.copy()
  points_copy.pop(point[2])
  total_distance = point[1]
  point = point[0]

  if(len(points_copy) < 5):
    k = len(points_copy)

  for i in range(k):
    near = get_near_point(point, points_copy)

    point = near[0]
    points_copy.remove(near[0])
    total_distance += near[1]

  return total_distance


def neartest_point(start, points, k=5):
  points_distances_index = []
  for i in range(len(points)):
    value = []
    (distance) = calculate_distance(start, points[i])

    value.append(points[i])
    value.append(distance)
    value.append(i)
    points_distances_index.append(value)
  
  sorted_points = sorted(points_distances_index, key=lambda x: x[1])
  avaliable_points = sorted_points[:k]

  for i in range(len(avaliable_points)):
    avaliable_points[i][1] = calculate_distance_of_next(avaliable_points[i], points)

  final_best = sorted(avaliable_points, key=lambda x: x[1])

  return final_best[0][0], final_best[0][2]



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