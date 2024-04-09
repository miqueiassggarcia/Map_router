import heapq
import json

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    previous_nodes = {}  # Keep track of previous nodes in the shortest path
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node == end:
            break
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                previous_nodes[neighbor] = current_node
    
    shortest_path = []
    current_node = end
    while current_node != start:
        shortest_path.append(current_node)
        current_node = previous_nodes[current_node]
    shortest_path.append(start)
    shortest_path.reverse()
    
    return shortest_path, distances[end]

def geojson_to_graph(geojson):
    graph = {}
    for feature in geojson['features']:
        node_id = feature['id']
        coordinates = feature['geometry']['coordinates']
        neighbors = {}
        for neighbor_feature in geojson['features']:
            neighbor_id = neighbor_feature['id']
            neighbor_coordinates = neighbor_feature['geometry']['coordinates']
            if node_id != neighbor_id:  # Avoid adding itself as a neighbor
                distance = calculate_distance(coordinates, neighbor_coordinates)
                neighbors[neighbor_id] = distance
        graph[node_id] = neighbors
    return graph

def calculate_distance(coord1, coord2):
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

with open('data/nodesvistaserrana.geojson') as f:
    geojson_data = json.load(f)

graph = geojson_to_graph(geojson_data)
start_node = "node/7641883305"
end_node = "node/7643639711"
shortest_path, distance = dijkstra(graph, start_node, end_node)
print("Shortest path:", shortest_path)
print("Distance:", distance)