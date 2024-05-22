import numpy as np
import matplotlib.pyplot as plt
import random
import math
from process_vs import graph

class AntColony:
    def __init__(self, graph, num_ants, num_iterations, decay, alpha=1, beta=1):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.nodes = list(graph.keys())
        self.pheromones = {node: {connected_node: 1.0 for connected_node in connections} for node, connections in graph.items()}
        
        # Ensure all pairs have a pheromone entry, even if no direct connection exists
        for node in self.nodes:
            for other_node in self.nodes:
                if other_node not in self.pheromones[node]:
                    self.pheromones[node][other_node] = 1.0

    def run(self, points):
        best_path = None
        best_path_length = float('inf')
        
        for _ in range(self.num_iterations):
            all_paths = self.construct_solutions(points)
            self.update_pheromones(all_paths)
            
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < best_path_length:
                best_path = shortest_path[0]
                best_path_length = shortest_path[1]
        
        return best_path, best_path_length

    def construct_solutions(self, points):
        all_paths = []
        for _ in range(self.num_ants):
            path = self.construct_solution(points)
            path_length = self.calculate_path_length(path)
            all_paths.append((path, path_length))
        return all_paths

    def construct_solution(self, points):
        path = [points[0]]
        current_node = points[0]
        points_to_visit = set(points[1:])
        
        while points_to_visit:
            next_node = self.select_next_node(current_node, path, points_to_visit)
            path.append(next_node)
            points_to_visit.remove(next_node)
            current_node = next_node
        
        path.append(points[0])  # return to start point to form a cycle
        return path

    def select_next_node(self, current_node, path, points_to_visit):
        probabilities = []
        total_pheromone = 0
        
        for neighbor in points_to_visit:
            pheromone = self.pheromones[current_node][neighbor] ** self.alpha
            heuristic = (1.0 / self.distance(current_node, neighbor)) ** self.beta
            probabilities.append((neighbor, pheromone * heuristic))
            total_pheromone += pheromone * heuristic
        
        probabilities = [(node, prob / total_pheromone) for node, prob in probabilities]
        r = random.uniform(0, 1)
        cumulative_probability = 0
        
        for node, prob in probabilities:
            cumulative_probability += prob
            if r <= cumulative_probability:
                return node
        
        return probabilities[-1][0]

    def calculate_path_length(self, path):
        length = 0
        for i in range(len(path) - 1):
            length += self.distance(path[i], path[i + 1])
        return length

    def distance(self, node1, node2):
        return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

    def update_pheromones(self, all_paths):
        for node in self.pheromones:
            for neighbor in self.pheromones[node]:
                self.pheromones[node][neighbor] *= (1 - self.decay)
        
        for path, path_length in all_paths:
            for i in range(len(path) - 1):
                self.pheromones[path[i]][path[i + 1]] += 1.0 / path_length
            self.pheromones[path[-1]][path[0]] += 1.0 / path_length  # to complete the cycle

def plot_path(graph, path):
    for node in graph:
        for connected_node in graph[node]:
            plt.plot([node[1], connected_node[1]], [node[0], connected_node[0]], 'k-', alpha=0.3)
    path_x = [node[1] for node in path]
    path_y = [node[0] for node in path]
    plt.plot(path_x, path_y, marker='o')
    plt.gca().invert_yaxis()
    plt.show()

def main():
    listOfNodes = list(graph.keys())

    # points = [listOfNodes[random.randint(0, len(listOfNodes)-1)] for _ in range(340)]
    points = listOfNodes
    
    colony = AntColony(graph, num_ants=10, num_iterations=100, decay=0.1, alpha=1, beta=5)
    best_path, best_length = colony.run(points)
    
    print("Best path:", best_path)
    print("Best path length:", best_length)
    
    plot_path(graph, best_path)

if __name__ == "__main__":
    main()
