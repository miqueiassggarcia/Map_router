import time
import numpy as np
import matplotlib.pyplot as plt
import random
from process_city import graphpatoscompleto, graphpatos, graphpatos4, graphpatos2, graphpatos1
from dijkstra import dijkstra

class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheromone(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path            
            self.pheromone *= self.decay            
        return all_time_shortest_path

    def spread_pheromone(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))  # going back to where we started    
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)
        row = np.nan_to_num(row, nan=0.0)
        if row.sum() == 0:
            norm_row = np.ones(len(row)) / len(row)
        else:
            norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move

def np_choice(a, size, replace=True, p=None):
    if p is not None:
        p = np.array(p)
        p = np.nan_to_num(p, nan=0.0)
        if p.sum() != 1.0:
            p /= p.sum()  # Ensure the probabilities sum to 1
    return np.random.choice(a, size, replace, p)

def create_distance_matrix(coordinates, graph):
    num_points = len(coordinates)
    distance_matrix = np.zeros((num_points, num_points))
    
    paths = {}
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                path, path_length = dijkstra(graph, coordinates[i], coordinates[j])
                paths[(i, j)] = path
                distance_matrix[i][j] = path_length
            else:
                distance_matrix[i][j] = np.inf  # Distance to self is set to infinity
    return paths, distance_matrix

list_nodes_patos_completo = list(graphpatoscompleto.keys())
list_nodes_patos = list(graphpatos.keys())
list_nodes_patos4 = list(graphpatos4.keys())
list_nodes_patos2 = list(graphpatos2.keys())
list_nodes_patos1 = list(graphpatos1.keys())

def teste(points, graph):
    start_algoritm = time.time()

    start_dijkstra_time = time.time()
    paths, distance_matrix = create_distance_matrix(points, graph)
    end_dijkstra_time = time.time()
    dijkstra_time = round(end_dijkstra_time - start_dijkstra_time, 3)

    start_aco_time = time.time()
    ant_colony = AntColony(distance_matrix, 10, 5, 100, 0.5, alpha=1, beta=1)
    shortest_path, shortest_distance = ant_colony.run()
    end_aco_time = time.time()
    aco_time = round(end_aco_time - start_aco_time, 3)

    final_points = []
    final_path = []
    for i in range(len(shortest_path) - 1):
        if(i == 0):
            final_points.append(points[shortest_path[i][0]])
            final_points.append(points[shortest_path[i][1]])
            final_path = final_path + paths[shortest_path[i]]
        else:
            final_points.append(points[shortest_path[i][1]])
            final_path.pop()
            final_path = final_path + paths[shortest_path[i]]

    end_algoritm = time.time()
    algoritm_time = round(end_algoritm - start_algoritm, 3)
    print(f"Algoritmo: {algoritm_time}s, \nDijkstra: {dijkstra_time}s, \nACO: {aco_time}s")

i = 5
# print("\nPatos Completo " + str(i) + " pontos")
# points_patos_completo = [list_nodes_patos_completo[random.randint(0, len(list_nodes_patos_completo)-1)] for _ in range(i)]
# teste(points_patos_completo, graphpatoscompleto)

# print("\nPatos Completo " + str(i*2) + " pontos")
# points_patos_completo = [list_nodes_patos_completo[random.randint(0, len(list_nodes_patos_completo)-1)] for _ in range(i*2)]
# teste(points_patos_completo, graphpatoscompleto)

# print("\nPatos Completo " + str(i*4) + " pontos")
# points_patos_completo = [list_nodes_patos_completo[random.randint(0, len(list_nodes_patos_completo)-1)] for _ in range(i*4)]
# teste(points_patos_completo, graphpatoscompleto)

# print("\nPatos Completo " + str(i*6) + " pontos")
# points_patos_completo = [list_nodes_patos_completo[random.randint(0, len(list_nodes_patos_completo)-1)] for _ in range(i*6)]
# teste(points_patos_completo, graphpatoscompleto)

# print("\nPatos Metropolitano " + str(i) + " pontos")
# points_patos = [list_nodes_patos[random.randint(0, len(list_nodes_patos)-1)] for _ in range(i)]
# teste(points_patos, graphpatos)

# print("\nPatos Metropolitano " + str(i*2) + " pontos")
# points_patos = [list_nodes_patos[random.randint(0, len(list_nodes_patos)-1)] for _ in range(i*2)]
# teste(points_patos, graphpatos)

# print("\nPatos Metropolitano " + str(i*4) + " pontos")
# points_patos = [list_nodes_patos[random.randint(0, len(list_nodes_patos)-1)] for _ in range(i*4)]
# teste(points_patos, graphpatos)

# print("\nPatos Metropolitano " + str(i*6) + " pontos")
# points_patos = [list_nodes_patos[random.randint(0, len(list_nodes_patos)-1)] for _ in range(i*6)]
# teste(points_patos, graphpatos)

# print("\nPatos Metropolitano " + "4km " + str(i) + " pontos")
# points_patos4 = [list_nodes_patos4[random.randint(0, len(list_nodes_patos4)-1)] for _ in range(i)]
# teste(points_patos4, graphpatos4)

# print("\nPatos Metropolitano " + "4km " + str(i*2) + " pontos")
# points_patos4 = [list_nodes_patos4[random.randint(0, len(list_nodes_patos4)-1)] for _ in range(i*2)]
# teste(points_patos4, graphpatos4)

# print("\nPatos Metropolitano " + "4km " + str(i*4) + " pontos")
# points_patos4 = [list_nodes_patos4[random.randint(0, len(list_nodes_patos4)-1)] for _ in range(i*4)]
# teste(points_patos4, graphpatos4)

# print("\nPatos Metropolitano " + "4km " + str(i*6) + " pontos")
# points_patos4 = [list_nodes_patos4[random.randint(0, len(list_nodes_patos4)-1)] for _ in range(i*6)]
# teste(points_patos4, graphpatos4)

# print("\nPatos Metropolitano " + "2km " + str(i) + " pontos")
# points_patos2 = [list_nodes_patos2[random.randint(0, len(list_nodes_patos2)-1)] for _ in range(i)]
# teste(points_patos2, graphpatos2)

# print("\nPatos Metropolitano " + "2km " + str(i*2) + " pontos")
# points_patos2 = [list_nodes_patos2[random.randint(0, len(list_nodes_patos2)-1)] for _ in range(i*2)]
# teste(points_patos2, graphpatos2)

# print("\nPatos Metropolitano " + "2km " + str(i*4) + " pontos")
# points_patos2 = [list_nodes_patos2[random.randint(0, len(list_nodes_patos2)-1)] for _ in range(i*4)]
# teste(points_patos2, graphpatos2)

# print("\nPatos Metropolitano " + "2km " + str(i*6) + " pontos")
# points_patos2 = [list_nodes_patos2[random.randint(0, len(list_nodes_patos2)-1)] for _ in range(i*6)]
# teste(points_patos2, graphpatos2)

print("\nPatos Metropolitano " + "1km " + str(i) + " pontos")
points_patos1 = [list_nodes_patos1[random.randint(0, len(list_nodes_patos1)-1)] for _ in range(i)]
teste(points_patos1, graphpatos1)

print("\nPatos Metropolitano " + "1km " + str(i*2) + " pontos")
points_patos1 = [list_nodes_patos1[random.randint(0, len(list_nodes_patos1)-1)] for _ in range(i*2)]
teste(points_patos1, graphpatos1)

print("\nPatos Metropolitano " + "1km " + str(i*4) + " pontos")
points_patos1 = [list_nodes_patos1[random.randint(0, len(list_nodes_patos1)-1)] for _ in range(i*4)]
teste(points_patos1, graphpatos1)

print("\nPatos Metropolitano " + "1km " + str(i*6) + " pontos")
points_patos1 = [list_nodes_patos1[random.randint(0, len(list_nodes_patos1)-1)] for _ in range(i*6)]
teste(points_patos1, graphpatos1)


# print(f"Final path: {final_points}")

# def plot_path(graph, path, points=None):
#     # Plot the edges of the graph
#     for node in graph:
#         for connected_node in graph[node]:
#             plt.plot([node[1], connected_node[1]], [node[0], connected_node[0]], 'k-', alpha=0.3)
    
#     # Extract path coordinates
#     path_x = [node[1] for node in path]
#     path_y = [node[0] for node in path]
    
#     # Plot the path lines
#     plt.plot(path_x, path_y)
    
#     # Plot the path points with red color
#     plt.scatter(path_x, path_y)
    
#     # Plot additional points if provided
#     if points:
#         points_x = [point[1] for point in points]
#         points_y = [point[0] for point in points]
#         plt.scatter(points_x, points_y, color='red', marker='o')
    
#     plt.scatter(points[0][1], points[0][0], color='green', marker='o')
#     plt.scatter(points[len(points)-1][1], points[len(points)-1][0], color='yellow', marker='o')
    
#     plt.gca().invert_yaxis()
    
#     plt.show()

# plot_path(graph, final_path, final_points)