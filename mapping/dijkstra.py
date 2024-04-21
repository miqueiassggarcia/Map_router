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