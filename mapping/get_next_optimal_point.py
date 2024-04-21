from dijkstra import calculate_distance

def get_near_point(start, points):
  near = [(float('inf'), float('inf')), (float('inf'))]
  for i in range(len(points)):
    (distance) = calculate_distance(start, points[i])
    if(distance < near[1] and distance != 0):
      near[0] = points[i]
      near[1] = distance
  
  return near

def calculate_distance_of_next(point, points, k=5):
  points_copy = points.copy()
  points_copy.pop(point[2])
  total_distance = point[1]
  point = point[0]

  if(len(points_copy) < 5):
    k = len(points_copy)

  for i in range(k):
    near = get_near_point(point, points_copy)

    point = near[0]
    points_copy.remove(near[0])
    total_distance += near[1]

  return total_distance


def neartest_point(start, points, k=5):
  points_distances_index = []
  for i in range(len(points)):
    value = []
    (distance) = calculate_distance(start, points[i])

    value.append(points[i])
    value.append(distance)
    value.append(i)
    points_distances_index.append(value)
  
  sorted_points = sorted(points_distances_index, key=lambda x: x[1])
  avaliable_points = sorted_points[:k]

  for i in range(len(avaliable_points)):
    avaliable_points[i][1] = calculate_distance_of_next(avaliable_points[i], points)

  final_best = sorted(avaliable_points, key=lambda x: x[1])

  return final_best[0][0], final_best[0][2]