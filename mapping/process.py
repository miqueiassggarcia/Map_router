import json
import time

start_time = time.time()

# Read GeoJSON file
with open('data/patos.geojson') as f:
  data = json.load(f)

# Extract nodes and their coordinates
graph = {}
for feature in data['features']:
  coords = feature['geometry']['coordinates']
  for i in range(len(coords)):
    node = tuple(coords[i])
    if(node not in graph):
      graph[node] = []

    if(i > 0):
      node0 = tuple(coords[i-1])
      if(node0 not in graph[node]):
        graph[node].append(node0)

    if(i < len(coords) - 1):
      node1 = tuple(coords[i+1])
      if(node1 not in graph[node]):
        graph[node].append(node1)

# Identify connections between nodes
# for feature in data['features']:
#   coords = feature['geometry']['coordinates']
#   for i in range(len(coords) - 1):
#     node = tuple(coords[i])
#     print(node)
#     print(nodes[node])

# # Write graph to JSON file
# with open('graph.json', 'w') as f:
#   json.dump(graph, f)

# import heapq

# def dijkstra(graph, start_node, end_node):
#     # Create a set to keep track of visited nodes
#     visited = set()
    
#     # Create a priority queue to store nodes based on their distances
#     priority_queue = [(0, start_node)]
    
#     # Create a dictionary to store distances from the start node
#     distances = {node: float('inf') for node in graph}
#     distances[start_node] = 0
    
#     # Create a dictionary to store the previous node in the shortest path
#     previous_nodes = {node: None for node in graph}
    
#     while priority_queue:
#         current_distance, current_node = heapq.heappop(priority_queue)
        
#         if current_node == end_node:
#             # Reached the end node, reconstruct the shortest path
#             path = []
#             while current_node is not None:
#                 path.append(current_node)
#                 current_node = previous_nodes[current_node]
#             return list(reversed(path)), distances[end_node]
        
#         # Mark the current node as visited
#         visited.add(current_node)
        
#         for neighbor_node in graph.get(current_node, []):
#             # Calculate the distance to the neighbor node
#             distance = current_distance + calculate_distance(current_node, neighbor_node)
            
#             # If the new distance is shorter
#             if distance < distances.get(neighbor_node, float('inf')):
#                 distances[neighbor_node] = distance
#                 previous_nodes[neighbor_node] = current_node
#                 heapq.heappush(priority_queue, (distance, neighbor_node))
    
#     # No path found
#     return None, float('inf')

# def calculate_distance(node1, node2):
#     # This function should calculate the distance between two nodes
#     # For simplicity, let's assume Euclidean distance in this example
#     x1, y1 = node1
#     x2, y2 = node2
#     return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

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

start = (-37.3058764, -7.0477253)
end = (-37.2668079, -7.0136892)

if start in graph and end in graph:
    path, distance = dijkstra(graph, start, end)
    if path is not None:
        print("Shortest path:", path)
        print("Shortest distance:", distance)
    else:
        print("No path found between the start and end nodes.")
else:
    print("Start or end node is not in the graph.")

nodes = [list(coordinates) for coordinates in path]


output = {
  "type": "FeatureCollection",
  "generator": "overpass-turbo",
  "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.",
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

with open("../web/output.json", "w") as json_file:
  json_file.write(output)

end_time = time.time()

execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")