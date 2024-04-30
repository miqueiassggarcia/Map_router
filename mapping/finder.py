import json

from mapping.dijkstra import dijkstra
from mapping.process import graph, data
from mapping.generate_points import generate_random_points
from mapping.get_next_optimal_point import neartest_point

def find_routes(packages):
  initial = (-37.2888462, -7.0266789)
  start = (-37.2888462, -7.0266789)
  pointsAux = {}
  points = []

  for i in range(len(packages)):
    pointsAux[packages[i]["coordinate"]] = i
    points.append(packages[i]["coordinate"])
  
  sequence = [start]
  nodes = []
  while len(points) > 0:
    end, index = neartest_point(start, points)
    points.pop(index)
    sequence.append(end)

    index_of_package = pointsAux[end]

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
              },
              "address": packages[index_of_package]["address"],
              "sender": packages[index_of_package]["sender"],
              "package": {
                "id": packages[index_of_package]["package"]["id"],
                "name": packages[index_of_package]["package"]["name"],
                "expresso": packages[index_of_package]["package"]["expresso"],
                "peso": float(packages[index_of_package]["package"]["peso"]),
                "volume": float(packages[index_of_package]["package"]["volume"]),
                "fragil": packages[index_of_package]["package"]["fragil"],
                "time": packages[index_of_package]["package"]["time"].strftime('%H:%M:%S'),
                "data": packages[index_of_package]["package"]["data"].strftime('%Y-%m-%d')
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