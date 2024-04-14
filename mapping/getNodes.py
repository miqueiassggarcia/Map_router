import requests
from finder import output_path, dijkstra
import json

with open('nodes.json') as f:
  nodes = json.load(f)

# Define the Overpass API endpoint
overpass_url = "http://overpass-api.de/api/interpreter"

# Define your Overpass query
overpass_query_initial = """
[out:json];
	(area["name"="Patos"]["place"="municipality"];)->.a;
	way
      ["highway"]
      ["highway"!="footway"]
      ["highway"!="bridleway"]
      ["highway"!="steps"]
      ["highway"!="path"]
      ["highway"!="cycleway"]
      ["highway"!="pedestrian"]
      ["highway"!="proposed"]
      ["highway"!="service"]
      ["highway"!="living_street"]
      ["highway"!="raceway"]
      [name="Rua Godofredo Medeiros"]
    (area.a);
	node(w);
out geom;
"""

overpass_query_end = """
[out:json];
	(area["name"="Patos"]["place"="municipality"];)->.a;
	way
      ["highway"]
      ["highway"!="footway"]
      ["highway"!="bridleway"]
      ["highway"!="steps"]
      ["highway"!="path"]
      ["highway"!="cycleway"]
      ["highway"!="pedestrian"]
      ["highway"!="proposed"]
      ["highway"!="service"]
      ["highway"!="living_street"]
      ["highway"!="raceway"]
      [name="Rua Alberto Lustosa"]
    (area.a);
	node(w);
out geom;
"""
# overpass_query = """
# [out:json];
# node(around:30, -6.7428120, -37.568187);
# out geom;
# """

# Define parameters for the HTTP POST request
payload = {
    "data": overpass_query_initial
}

# Make the HTTP POST request to the Overpass API
response1 = requests.post(overpass_url, data=payload)

payload = {
    "data": overpass_query_end
}

response2 = requests.post(overpass_url, data=payload)

# Check if the request was successful (status code 200)
if response1.status_code == 200 and response2.status_code == 200:
    # Print the JSON response
    # print(response.json())
    data1 = response1.json()
    data2 = response2.json()
    node1 = data1["elements"][int(len(data1["elements"])/2)]
    node2 = data2["elements"][int(len(data2["elements"])/2)]

    shortest_path, shortest_distance = dijkstra(nodes, "node/" + str(node1["id"]), "node/" + str(node2["id"]))
    output_path(shortest_path)
else:
    # Print an error message
    print("Error:", response1.status_code)
    print("Error:", response2.status_code)