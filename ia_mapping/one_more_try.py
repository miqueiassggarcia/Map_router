import random
import numpy as np

# Parameters
alpha = 1.0  # Influence of pheromone
beta = 2.0   # Influence of heuristic value (distance)
evaporation_rate = 0.5
ant_count = 10
iterations = 100
pheromone_initial = 1.0
pheromone_increase = 1.0

def calculate_distance(graph, path):
    # Calculate the total distance of a path in the graph
    distance = 0
    for i in range(len(path) - 1):
        distance += graph[path[i]][path[i + 1]]
    return distance

def choose_next_node(current_node, unvisited_nodes, pheromone, graph):
    # Choose the next node based on pheromone levels and heuristic information
    probabilities = []
    for next_node in unvisited_nodes:
        pheromone_level = pheromone[(current_node, next_node)]
        heuristic_value = 1.0 / calculate_distance(graph, [current_node, next_node])
        probabilities.append((next_node, (pheromone_level ** alpha) * (heuristic_value ** beta)))

    if not probabilities:
        print("No valid moves")
        return None  # No valid moves

    total = sum(prob for _, prob in probabilities)
    probabilities = [(node, prob / total) for node, prob in probabilities]

    nodes, probs = zip(*probabilities)
    return np.random.choice(nodes, p=probs)

def aco(graph, start, points_to_visit):
    # Initialize pheromone levels
    pheromone = {(node1, node2): pheromone_initial for node1 in graph for node2 in graph[node1]}


    best_path = None
    best_length = float('inf')

    for _ in range(iterations):
        paths = []
        lengths = []

        for _ in range(ant_count):
            path = [start]
            unvisited_nodes = set(points_to_visit) - {start}
            current_node = start

            while unvisited_nodes:
                next_node = choose_next_node(current_node, unvisited_nodes, pheromone, graph)
                if next_node is None:
                    break  # No valid next node, break out of the loop
                path.append(next_node)
                unvisited_nodes.remove(next_node)
                current_node = next_node

            path.append(start)  # Returning to the starting node
            paths.append(path)
            lengths.append(calculate_distance(graph, path))

        # Update pheromones
        for i, path in enumerate(paths):
            for j in range(len(path) - 1):
                pheromone[(path[j], path[j + 1])] += pheromone_increase / lengths[i]
                pheromone[(path[j + 1], path[j])] += pheromone_increase / lengths[i]  # Add pheromone for the reverse edge

        # Evaporate pheromones
        for edge in pheromone:
            pheromone[edge] *= (1 - evaporation_rate)

        # Update the best path
        min_length = min(lengths)
        if min_length < best_length:
            best_length = min_length
            best_path = paths[lengths.index(min_length)]

    return best_path, best_length

# Example usage
graph = {
    'A': {'B': 1, 'C': 2, 'D': 3},
    'B': {'C': 2, 'E': 4},
    'C': {'D': 1, 'E': 2},
    'D': {'E': 3},
    'E': {}
}

start_node = 'A'
points_to_visit = ['B', 'C', 'D', 'E']

best_path, best_length = aco(graph, start_node, points_to_visit)
print("Best path:", best_path)
print("Best length:", best_length)
