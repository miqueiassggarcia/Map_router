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

    for connections in self.graph.values():
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

colony = AntColony(graph, num_ants=10, num_iterations=100, decay=0.1, alpha=1, beta=5)