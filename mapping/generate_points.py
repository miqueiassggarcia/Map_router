import random

def generate_random_points(points, data):
  for i in range(10):
    random_int = random.randint(0, len(data["features"]))
    way = data["features"][random_int]["geometry"]["coordinates"]
    point = way[random.randint(0, len(way) - 1)]
    points.append(tuple(point))