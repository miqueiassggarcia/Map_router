import json

with open('data/nodestabira.geojson') as f:
  nodespatos = json.load(f)

with open('data/tabira.geojson') as f:
  wayspatos = json.load(f)

# i = 0
# j = 0

# list_of_ways = []

# for i in wayspatos["features"]:
#   item = {
#     "way": {
#       "id": i["properties"]["@id"],
#       "nodes": []
#     }
#   }
#   for j in range(0, len(i["geometry"]["coordinates"])):
#     node = {
#       "node": i["geometry"]["coordinates"][j],
#       "connections": []
#     }
#     for w in wayspatos["features"]:
#       if(i["geometry"]["coordinates"][j] in w["geometry"]["coordinates"] and i["properties"]["@id"] != w["properties"]["@id"]):
#         node["connections"].append([w["properties"]["@id"], w["geometry"]["coordinates"].index(i["geometry"]["coordinates"][j])])
#     if(j == len(i["geometry"]["coordinates"])-1):
#       node["connections"].append(i["geometry"]["coordinates"][j-1])
#       item["way"]["nodes"].append(node)
#     elif(j == 0):
#       node["connections"].append(i["geometry"]["coordinates"][j+1])
#       item["way"]["nodes"].append(node)
#     else:
#       node["connections"].append(i["geometry"]["coordinates"][j-1])
#       node["connections"].append(i["geometry"]["coordinates"][j+1])
#       item["way"]["nodes"].append(node)
#   list_of_ways.append(item)

# json_data = json.dumps(list_of_ways, indent=4)

# with open("ways.json", "w") as json_file:
#   json_file.write(json_data)

list_of_nodes = []

for feature in wayspatos["features"]:
  for i in range(0, len(feature["geometry"]["coordinates"])):
    node = [feature["geometry"]["coordinates"][i]]

    for verifyfeature in wayspatos["features"]:
      if(feature["geometry"]["coordinates"][i] in verifyfeature["geometry"]["coordinates"] and feature["properties"]["@id"] != verifyfeature["properties"]["@id"]):
        index = verifyfeature["geometry"]["coordinates"].index(feature["geometry"]["coordinates"][i])
        if(index == 0):
          node.append(verifyfeature["geometry"]["coordinates"][index+1])
        elif(index == len(verifyfeature["geometry"]["coordinates"])-1):
          node.append(verifyfeature["geometry"]["coordinates"][index-1])
        else:
          node.append(verifyfeature["geometry"]["coordinates"][index-1])
          node.append(verifyfeature["geometry"]["coordinates"][index+1])

    if(i == len(feature["geometry"]["coordinates"])-1):
      node.append(feature["geometry"]["coordinates"][i-1])
    elif(i == 0):
      node.append(feature["geometry"]["coordinates"][i+1])
    else:
      node.append(feature["geometry"]["coordinates"][i-1])
      node.append(feature["geometry"]["coordinates"][i+1])

    if(len(node) > 1):
      list_of_nodes.append(node)

# nodes = {
#   "nodes": list_of_nodes
# }

nodes = []

for current_node in list_of_nodes:
  node = {
      "id": "",
      "coordinates": [],
      "connections": []
  }
  connections = []

  for feature in nodespatos["features"]:
    if(feature["geometry"]["coordinates"] == current_node[0]):
      node["id"] = feature["id"]
      node["coordinates"] = feature["geometry"]["coordinates"]
    else:
      for i in range(1, len(current_node)):
        if(feature["geometry"]["coordinates"] == current_node[i]):
          connections.append({
            "id": feature["id"],
            "coordinates": feature["geometry"]["coordinates"]
          })

  node["connections"] = connections

  if(len(node["id"]) > 0):
    nodes.append(node)


json_data2 = json.dumps(nodes, indent=4)

with open("nodestabira.json", "w") as json_file:
  json_file.write(json_data2)