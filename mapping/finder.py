import json

from mapping.dijkstra import dijkstra
from mapping.process import graph, data
from mapping.generate_points import generate_random_points
from mapping.get_next_optimal_point import neartest_point

def find_routes():
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
          values = [list(coordinates) for coordinates in path]
          nodes.append(
            {
              "type": "Feature",
              "geometry": {
                "type": "LineString",
                "coordinates": values
              }
            }
          )
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
    "features": nodes
  }

  return output