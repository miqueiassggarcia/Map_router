# import heapq
import json

# def dijkstra(nodes, start_id, end_id):
#     # Create a dictionary to store distances from the start node
#     distances = {node["id"]: float('inf') for node in nodes}
#     distances[start_id] = 0
    
#     # Create a dictionary to store the previous node in the shortest path
#     previous_nodes = {node["id"]: None for node in nodes}
    
#     # Create a priority queue to store nodes based on their distances
#     priority_queue = [(0, start_id)]
    
#     try:
#         while priority_queue:
#             current_distance, current_id = heapq.heappop(priority_queue)
            
#             if current_id == end_id:
#                 # Reached the end node, reconstruct the shortest path
#                 path = []
#                 while current_id is not None:
#                     path.append(current_id)
#                     current_id = previous_nodes[current_id]
#                 return list(reversed(path)), distances[end_id]
            
#             for connection in next((node["connections"] for node in nodes if node["id"] == current_id), []):
#                 neighbor_id = connection["id"]
#                 distance = current_distance + calculate_distance(current_id, neighbor_id)
                
#                 if distance < distances[neighbor_id]:
#                     distances[neighbor_id] = distance
#                     previous_nodes[neighbor_id] = current_id
#                     heapq.heappush(priority_queue, (distance, neighbor_id))
#     except Exception as e:
#         print("Error occurred:", e)
    
#     # No path found
#     return None, float('inf')

# def calculate_distance(node1_id, node2_id):
#     # This function should calculate the distance between two nodes
#     # You can implement your own distance calculation based on coordinates
#     # For simplicity, let's assume Euclidean distance in this example
#     node1 = next((node for node in nodes if node["id"] == node1_id), None)
#     node2 = next((node for node in nodes if node["id"] == node2_id), None)
#     if node1 and node2:
#         return ((node1["coordinates"][0] - node2["coordinates"][0]) ** 2 + 
#                 (node1["coordinates"][1] - node2["coordinates"][1]) ** 2) ** 0.5
#     return float('inf')  # Return infinity if nodes are not found

import heapq

def dijkstra(nodes, start_id, end_id):
    # Create a dictionary to store distances from the start node
    distances = {node["id"]: float('inf') for node in nodes}
    distances[start_id] = 0
    
    # Create a dictionary to store the previous node in the shortest path
    previous_nodes = {node["id"]: None for node in nodes}
    
    # Create a priority queue to store nodes based on their distances
    priority_queue = [(0, start_id)]
    
    while priority_queue:
        current_distance, current_id = heapq.heappop(priority_queue)
        
        if current_id == end_id:
            # Reached the end node, reconstruct the shortest path
            path = []
            while current_id is not None:
                path.append(current_id)
                current_id = previous_nodes[current_id]
            return list(reversed(path)), distances[end_id]
        
        for connection in next((node["connections"] for node in nodes if node["id"] == current_id), []):
            neighbor_id = connection["id"]
            distance = current_distance + calculate_distance(current_id, neighbor_id)
            
            if distance < distances[neighbor_id]:
                distances[neighbor_id] = distance
                previous_nodes[neighbor_id] = current_id
                heapq.heappush(priority_queue, (distance, neighbor_id))
    
    # No path found
    return None, float('inf')

def calculate_distance(node1_id, node2_id):
    # This function should calculate the distance between two nodes
    # You can implement your own distance calculation based on coordinates
    # For simplicity, let's assume Euclidean distance in this example
    node1 = next((node for node in nodes if node["id"] == node1_id), None)
    node2 = next((node for node in nodes if node["id"] == node2_id), None)
    if node1 and node2:
        return ((node1["coordinates"][0] - node2["coordinates"][0]) ** 2 + 
                (node1["coordinates"][1] - node2["coordinates"][1]) ** 2) ** 0.5
    return float('inf')  # Return infinity if nodes are not found

start_id = "node/1826800840"
end_id = "node/1828174813"

with open('nodes.json') as f:
  nodes = json.load(f)

shortest_path, shortest_distance = dijkstra(nodes, start_id, end_id)
print("Shortest path:", shortest_path)
print("Shortest distance:", shortest_distance)