import numpy as np
import random
import math
from process import graph

class AntColony:
    def __init__(self, graph, num_ants, num_iterations, decay, alpha=1, beta=1):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.nodes = list(graph.keys())
        
        # Initialize pheromones in the graph structure
        for connections in graph.values():
            for connection in connections:
                connection['pheromone'] = 1.0

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
            connection = next((conn for conn in self.graph[current_node] if conn['connect_to'] == neighbor), None)
            if connection:
                pheromone = connection['pheromone'] ** self.alpha
                heuristic = (1.0 / connection['distance']) ** self.beta
                probabilities.append((neighbor, pheromone * heuristic))
                total_pheromone += pheromone * heuristic
        
        if not probabilities:
            return random.choice(list(points_to_visit))
        
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
            connection = next((conn for conn in self.graph[path[i]] if conn['connect_to'] == path[i + 1]), None)
            if connection:
                length += connection['distance']
        return length

    def update_pheromones(self, all_paths):
        # Decay existing pheromones
        for node, connections in self.graph.items():
            for conn in connections:
                conn['pheromone'] *= (1 - self.decay)
        
        # Add new pheromones based on paths
        for path, path_length in all_paths:
            for i in range(len(path) - 1):
                connection = next((conn for conn in self.graph[path[i]] if conn['connect_to'] == path[i + 1]), None)
                if connection:
                    connection['pheromone'] += 1.0 / path_length
            # Complete the cycle
            connection = next((conn for conn in self.graph[path[-1]] if conn['connect_to'] == path[0]), None)
            if connection:
                connection['pheromone'] += 1.0 / path_length

def main():
    # Example dictionary of global coordinates
    # graph = {
    #     (-37.2837219, -7.0518095): [(-37.2837701, -7.0517908), (-37.2836199, -7.0518414)],
    #     (-37.2837701, -7.0517908): [(-37.2837219, -7.0518095), (-37.2836199, -7.0518414)],
    #     (-37.2836199, -7.0518414): [(-37.2837219, -7.0518095), (-37.2837701, -7.0517908)]
    #     # Add more nodes and their connections as needed
    # }
    
    listOfNodes = list(graph.keys())

    points = [listOfNodes[random.randint(0, len(listOfNodes)-1)] for _ in range(10)]
    print(points)
    
    colony = AntColony(graph, num_ants=10, num_iterations=100, decay=0.1, alpha=1, beta=5)
    best_path, best_length = colony.run(points)
    
    print("Best path:", best_path)
    print("Best path length:", best_length)
    
main()
