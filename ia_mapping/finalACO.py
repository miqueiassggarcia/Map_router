import numpy as np
import matplotlib.pyplot as plt
import random
from ia_mapping.process_city import graph
from ia_mapping.dijkstra import dijkstra

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

def create_distance_matrix(coordinates):
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

def finder(packages):
    start = (-37.2888462, -7.0266789)
    points = [start]

    # print(len(packages))

    for i in range(len(packages)):
        if(packages[i]["coordinate"] in graph):
            points.append(packages[i]["coordinate"])
    
    # print(points)
    
    paths, distance_matrix = create_distance_matrix(points)

    ant_colony = AntColony(distance_matrix, 10, 5, 100, 0.5, alpha=1, beta=1)
    shortest_path, shortest_distance = ant_colony.run()
    # print(f"Shortest path: {shortest_path}")
    # print(f"Shortest distance: {shortest_distance}")

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
        
    if final_points is not None:
        print("Best path:", final_points)
        index_of_package = 0

        for path, next_path in zip(final_points[:-1], final_points[1:]):
            for i in range(len(packages)):
                if(packages[i]["coordinate"] == path):
                    index_of_package = i
                    break
            listOfCoordinates = [final_path[0]]
            for path2 in final_path:
                if(path2 == next_path):
                    break
                listOfCoordinates.append(path2)
            
            print("path, next_path: " + str(path) + ", " + str(next_path))

            nodes = []

            nodes.append(
            {
                "type": "Feature",
                "geometry": {
                "type": "LineString",
                "coordinates": listOfCoordinates
                },
                "address": packages[index_of_package]["address"],
                "sender": packages[index_of_package]["sender"],
                "package": {
                "id": packages[index_of_package]["package"]["id"],
                "name": packages[index_of_package]["package"]["name"],
                "expresso": packages[index_of_package]["package"]["expresso"],
                "peso": float(packages[index_of_package]["package"]["peso"]),
                "volume": float(packages[index_of_package]["package"]["volume"]),
                "fragil": packages[index_of_package]["package"]["fragil"],
                "time": packages[index_of_package]["package"]["time"].strftime('%H:%M:%S'),
                "data": packages[index_of_package]["package"]["data"].strftime('%Y-%m-%d')
                }
            }
            )
    else:
        print("No path found.")

    # print(nodes)

    output = {
        "type": "FeatureCollection",
        "generator": "overpass-turbo",
        "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.",
        "sequence": final_points,
        "features": nodes
    }

    return output

# listOfNodes = list(graph.keys())
# points = [listOfNodes[random.randint(0, len(listOfNodes)-1)] for _ in range(10)]

# paths, distance_matrix = create_distance_matrix(points)

# ant_colony = AntColony(distance_matrix, 10, 5, 100, 0.5, alpha=1, beta=1)
# shortest_path, shortest_distance = ant_colony.run()
# # print(f"Shortest path: {shortest_path}")
# # print(f"Shortest distance: {shortest_distance}")

# final_points = []
# final_path = []
# for i in range(len(shortest_path) - 1):
#     if(i == 0):
#         final_points.append(points[shortest_path[i][0]])
#         final_points.append(points[shortest_path[i][1]])
#         final_path = final_path + paths[shortest_path[i]]
#     else:
#         final_points.append(points[shortest_path[i][1]])
#         final_path.pop()
#         final_path = final_path + paths[shortest_path[i]]



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

# print(final_path)
# plot_path(graph, final_path, final_points)