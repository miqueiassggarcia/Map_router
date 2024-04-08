import json

from shapely.geometry import Point, mapping, shape
from shapely.ops import nearest_points

with open("patos copy.geojson") as f:
    geojson = json.load(f)

ref_point = Point(-37.2900, -7.0300)

features = []
min_distance = None
min_index = None

for i, feature in enumerate(geojson["features"]):

    # Could be improved with Haversine distance, or distance in UTM coordinates for example
    p1, p2 = nearest_points(shape(feature["geometry"]), ref_point)
    distance = p1.distance(p2)

    if min_distance is None or distance < min_distance:
        min_distance = distance
        min_index = i

    feature["properties"] = {"index": i, "distance": distance}
    features.append(feature)
    features.append(
        {
            "type": "Feature",
            "properties": {"index": f"closest_point_{i}", "distance": distance},
            "geometry": mapping(p1),
        }
    )

features = sorted(features, key=lambda x: x["properties"]["distance"])

features.append(
    {
        "type": "Feature",
        "properties": {"index": "ref_point", "distance": 0},
        "geometry": mapping(ref_point),
    }
)

with open("gg.geojson", "w") as f:
    json.dump({"type": "FeatureCollection", "features": features}, f)