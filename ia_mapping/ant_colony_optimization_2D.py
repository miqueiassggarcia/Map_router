import numpy as np
import matplotlib.pyplot as plt
import random

class AntColony:
  def __init__(self, num_ants, num_iterations, decay, alpha=1, beta=1):
    self.num_ants = num_ants
    self.num_iterations = num_iterations
    self.decay = decay
    self.alpha = alpha
    self.beta = beta

  def initialize_pheromones(self, graph):
    self.pheromones = np.ones(graph.shape)

  def run(self, graph, start, end):
    self.graph = graph
    self.num_nodes = len(graph)
    self.start = start
    self.end = end
    self.initialize_pheromones(graph)
    
    best_path = None
    best_path_length = float('inf')
        
    for iteration in range(self.num_iterations):
      all_paths = self.construct_solutions()
      self.update_pheromones(all_paths)
      
      shortest_path = min(all_paths, key=lambda x: x[1])
      if shortest_path[1] < best_path_length:
        best_path = shortest_path[0]
        best_path_length = shortest_path[1]
    
    return best_path, best_path_length

  def construct_solutions(self):
    all_paths = []
    for _ in range(self.num_ants):
      path = self.construct_solution(self.start)
      path_length = self.calculate_path_length(path)
      all_paths.append((path, path_length))
    return all_paths

  def construct_solution(self, start):
    path = [start]
    current_node = start
    
    while current_node != self.end:
      next_node = self.select_next_node(current_node, path)
      path.append(next_node)
      current_node = next_node
    
    return path

  def select_next_node(self, current_node, path):
    probabilities = []
    total_pheromone = 0
    
    for neighbor in range(self.num_nodes):
      if neighbor not in path and self.graph[current_node][neighbor] > 0:
        pheromone = self.pheromones[current_node][neighbor] ** self.alpha
        heuristic = (1.0 / self.graph[current_node][neighbor]) ** self.beta
        probabilities.append((neighbor, pheromone * heuristic))
        total_pheromone += pheromone * heuristic
    
    if total_pheromone == 0:
      return random.choice([i for i in range(self.num_nodes) if i not in path])
    
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
      length += self.graph[path[i]][path[i + 1]]
    return length

  def update_pheromones(self, all_paths):
    self.pheromones *= (1 - self.decay)
    for path, path_length in all_paths:
      for i in range(len(path) - 1):
        self.pheromones[path[i]][path[i + 1]] += 1.0 / path_length

def plot_path(graph, path):
  plt.imshow(graph, cmap='gray_r')
  path_x = [x[1] for x in path]
  path_y = [x[0] for x in path]
  plt.plot(path_x, path_y, marker='o')
  plt.show()

def main():
  grid_size = 10
  graph = np.ones((grid_size, grid_size))

  # Create random obstacles in the grid
  num_obstacles = 20
  for _ in range(num_obstacles):
    x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
    graph[x, y] = np.inf

  start = (0, 0)
  end = (grid_size - 1, grid_size - 1)
  
  # Flatten the 2D grid into a 1D graph representation
  graph_1d = np.zeros((grid_size * grid_size, grid_size * grid_size))
  for i in range(grid_size):
    for j in range(grid_size):
      if graph[i, j] == np.inf:
        continue
      current_node = i * grid_size + j
      if i + 1 < grid_size and graph[i + 1, j] != np.inf:
        graph_1d[current_node][current_node + grid_size] = 1
      if i - 1 >= 0 and graph[i - 1, j] != np.inf:
        graph_1d[current_node][current_node - grid_size] = 1
      if j + 1 < grid_size and graph[i, j + 1] != np.inf:
        graph_1d[current_node][current_node + 1] = 1
      if j - 1 >= 0 and graph[i, j - 1] != np.inf:
        graph_1d[current_node][current_node - 1] = 1
  
  colony = AntColony(num_ants=10, num_iterations=100, decay=0.1, alpha=1, beta=5)
  best_path, best_length = colony.run(graph_1d, start[0] * grid_size + start[1], end[0] * grid_size + end[1])

  # Convert the best path back to 2D coordinates
  best_path_coords = [(node // grid_size, node % grid_size) for node in best_path]
  
  plot_path(graph, best_path_coords)

main()
