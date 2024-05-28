import math
import random
import matplotlib.pyplot as plt
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
        self.pheromones = {node: {neighbor: 1.0 for neighbor in neighbors} for node, neighbors in graph.items()}

    def run(self, points):
        best_path = None
        best_path_length = float('inf')
        best_path_edges = None
        
        for _ in range(self.num_iterations):
            all_paths, all_edges = self.construct_solutions(points)
            if all_paths:
                shortest_path = min(all_paths, key=lambda x: x[1])
                if shortest_path[1] < best_path_length:
                    best_path = shortest_path[0]
                    best_path_length = shortest_path[1]
                    best_path_edges = all_edges[all_paths.index(shortest_path)]
            
        return best_path, best_path_length, best_path_edges

    def construct_solutions(self, points):
        all_paths = []
        all_edges = []
        for _ in range(self.num_ants):
            path, edges = self.construct_solution(points)
            path_length = self.calculate_path_length(edges)
            if path_length > 0:
                all_paths.append((path, path_length))
                all_edges.append(edges)
        return all_paths, all_edges

    def construct_solution(self, points):
        path = [points[0]]
        edges = []
        current_node = points[0]
        points_to_visit = set(points[1:])
        
        while points_to_visit:
            next_node, edge = self.select_next_node(current_node, points_to_visit)
            if next_node is None:
                break
            path.append(next_node)
            edges.append(edge)
            points_to_visit.remove(next_node)
            current_node = next_node
        
        if len(path) > 1 and path[0] in self.graph[path[-1]]:
            path.append(points[0])  # return to start point to form a cycle
            edges.append((path[-2], path[-1]))  # add the edge connecting the last and first nodes
        return path, edges

    def select_next_node(self, current_node, points_to_visit):
        probabilities = []
        total_pheromone = 0
        
        for neighbor in points_to_visit:
            if neighbor in self.graph[current_node]:
                pheromone = self.pheromones[current_node][neighbor] ** self.alpha
                heuristic = (1.0 / self.distance(current_node, neighbor)) ** self.beta
                probabilities.append((neighbor, pheromone * heuristic, (current_node, neighbor)))
                total_pheromone += pheromone * heuristic
        
        if not probabilities:
            return None, None
        
        probabilities = [(node, prob / total_pheromone, edge) for node, prob, edge in probabilities]
        r = random.uniform(0, 1)
        cumulative_probability = 0
        
        for node, prob, edge in probabilities:
            cumulative_probability += prob
            if r <= cumulative_probability:
                return node, edge
        
        return probabilities[-1][0], probabilities[-1][2]

    def calculate_path_length(self, edges):
        length = 0
        for edge in edges:
            length += self.distance(edge[0], edge[1])
        return length

    def distance(self, node1, node2):
        return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

    def update_pheromones(self, all_paths):
        for node in self.pheromones:
            for neighbor in self.pheromones[node]:
                self.pheromones[node][neighbor] *= (1 - self.decay)
        
        for path, path_length in all_paths:
            pheromone_amount = 1.0 / path_length if path_length > 0 else 0
            for i in range(len(path) - 1):
                self.add_pheromone(path[i], path[i + 1], pheromone_amount)
            if path[-1] in self.graph[path[0]]:
                self.add_pheromone(path[-1], path[0], pheromone_amount)  # to complete the cycle

    def add_pheromone(self, node1, node2, amount):
        if node2 in self.pheromones[node1]:
            self.pheromones[node1][node2] += amount
        if node1 in self.pheromones[node2]:
            self.pheromones[node2][node1] += amount

def plot_path(graph, path):
    for node in graph:
        for connected_node in graph[node]:
            plt.plot([node[1], connected_node[1]], [node[0], connected_node[0]], 'k-', alpha=0.3)
    path_x = [node[1] for node in path]
    path_y = [node[0] for node in path]
    plt.plot(path_x, path_y, marker='o')
    plt.gca().invert_yaxis()
    plt.show()


listOfNodes = list(graph.keys())

points = [listOfNodes[random.randint(0, len(listOfNodes)-1)] for _ in range(10)]

colony = AntColony(graph, num_ants=10, num_iterations=100, decay=0.1, alpha=1, beta=5)
best_path, best_length, best_path_edges = colony.run(points)

print("Best path:", best_path)
print("Best path length:", best_length)
print("Best path length edges:", best_path_edges)

plot_path(graph, best_path_edges)
