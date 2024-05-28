import random
import numpy as np
from process_vs import graph

# Parameters
alpha = 1.0  # Influence of pheromone
beta = 2.0   # Influence of heuristic value (distance)
evaporation_rate = 0.5
ant_count = 10
iterations = 100
pheromone_initial = 1.0
pheromone_increase = 1.0

# Initialize pheromone levels
pheromone = {(node, neighbor): pheromone_initial for node in graph for neighbor in graph[node]}

def calculate_distance(coordinates1, coordinates2):
    # Euclidean distance calculation
    return ((coordinates1[0] - coordinates2[0]) ** 2 + 
            (coordinates1[1] - coordinates2[1]) ** 2) ** 0.5

def choose_next_node(current_node, unvisited_nodes, pheromone, graph):
    probabilities = []
    for next_node in unvisited_nodes:
        if next_node in graph[current_node]:
            pheromone_level = pheromone[(current_node, next_node)]
            heuristic_value = 1.0 / calculate_distance(current_node, next_node)
            probabilities.append((next_node, (pheromone_level ** alpha) * (heuristic_value ** beta)))
    
    if not probabilities:
        print("No valid moves")
        quit()
        return None  # No valid moves
    
    total = sum(prob for _, prob in probabilities)
    if total == 0:
        return random.choice(list(unvisited_nodes))
    
    probabilities = [(node, prob / total) for node, prob in probabilities]
    print(probabilities)
    quit()

    nodes, probs = zip(*probabilities)

    # Convert nodes and probs to 1-dimensional numpy arrays
    nodes = np.array(nodes)
    probs = np.array(probs)
    
    # Debugging print statements
    print("Current Node:", current_node)
    print("Unvisited Nodes:", unvisited_nodes)
    print("Probabilities:", probabilities)
    print("Nodes:", nodes)
    print("Probs:", probs)
    
    return np.random.choice(nodes, p=probs)

def aco(graph, start, points_to_visit):
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
            lengths.append(sum(calculate_distance(path[i], path[i+1]) for i in range(len(path) - 1)))

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

# Run the ACO algorithm
start = (-37.5679019, -6.7443271)
listOfNodes = list(graph.keys())
points_to_visit = [listOfNodes[random.randint(0, len(listOfNodes)-1)] for _ in range(10)]

best_path, best_length = aco(graph, start, points_to_visit)

print("Best path found:", best_path)
print("Length of the best path:", best_length)