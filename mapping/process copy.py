import json
import time

start_time = time.time()

# Read GeoJSON file
with open('data/saopaulo.geojson') as f:
  data = json.load(f)

# Extract nodes and their coordinates
graph = {}
for feature in data['features']:
  coords = feature['geometry']['coordinates']
  for i in range(len(coords[0])):
    node = tuple(coords[0][i])
    if(node not in graph):
      graph[node] = []

    if(i > 0):
      node0 = tuple(coords[0][i-1])
      if(node0 not in graph[node]):
        graph[node].append(node0)

    if(i < len(coords[0]) - 1):
      node1 = tuple(coords[0][i+1])
      if(node1 not in graph[node]):
        graph[node].append(node1)

import heapq

def dijkstra(nodes, start_coordinates, end_coordinates):
    # Create a dictionary to store distances from the start node
    distances = {coordinates: float('inf') for coordinates in nodes}
    distances[start_coordinates] = 0
    
    # Create a dictionary to store the previous node in the shortest path
    previous_nodes = {coordinates: None for coordinates in nodes}
    
    # Create a priority queue to store nodes based on their distances
    priority_queue = [(0, start_coordinates)]
    
    while priority_queue:
        current_distance, current_coordinates = heapq.heappop(priority_queue)
        
        if current_coordinates == end_coordinates:
            # Reached the end node, reconstruct the shortest path
            path = []
            while current_coordinates is not None:
                path.append(current_coordinates)
                current_coordinates = previous_nodes[current_coordinates]
            return list(reversed(path)), distances[end_coordinates]
        
        for neighbor_coordinates in nodes[current_coordinates]:
            distance = current_distance + calculate_distance(current_coordinates, neighbor_coordinates)
            if distance < distances[neighbor_coordinates]:
                distances[neighbor_coordinates] = distance
                previous_nodes[neighbor_coordinates] = current_coordinates
                heapq.heappush(priority_queue, (distance, neighbor_coordinates))
    
    # No path found
    return None, float('inf')

def calculate_distance(coordinates1, coordinates2):
    # Euclidean distance calculation
    return ((coordinates1[0] - coordinates2[0]) ** 2 + 
            (coordinates1[1] - coordinates2[1]) ** 2) ** 0.5

initial = (-46.6506366, -23.6022019)
start = (-46.6506366, -23.6022019)
points = [
  (-46.7132759, -23.5713606)
]

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
      if(start != initial):
        path.pop(0)
      if path is not None:
        nodes += [list(coordinates) for coordinates in path]
      else:
          print("No path found between the start and end nodes.")
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