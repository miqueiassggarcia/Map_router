from dijkstra import calculate_distance

def neartest_point(start, points):
  current_end = [(float('inf'), float('inf')), (float('inf')), 0]
  for i in range(len(points)):
    (distance) = calculate_distance(start, points[i])
    if(distance < current_end[1]):
      current_end[0] = points[i]
      current_end[1] = distance
      current_end[2] = i

  return current_end[0], current_end[2]