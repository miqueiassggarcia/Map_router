import json

with open('data/nodespatos.geojson') as f:
  nodespatos = json.load(f)

with open('data/patos.geojson') as f:
  wayspatos = json.load(f)

i = 0
j = 0

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

for i in wayspatos["features"]:
  for j in range(0, len(i["geometry"]["coordinates"])):
    node = [i["geometry"]["coordinates"][j]]

    for w in wayspatos["features"]:
      if(i["geometry"]["coordinates"][j] in w["geometry"]["coordinates"] and i["properties"]["@id"] != w["properties"]["@id"]):
        index = w["geometry"]["coordinates"].index(i["geometry"]["coordinates"][j])
        if(index == 0):
          node.append([w["geometry"]["coordinates"][index+1]])
        elif(index == len(w["geometry"]["coordinates"])-1):
          node.append([w["geometry"]["coordinates"][index-1]])
        else:
          node.append([w["geometry"]["coordinates"][index-1], w["geometry"]["coordinates"][index+1]])

    if(j == len(i["geometry"]["coordinates"])-1):
      node.append([i["geometry"]["coordinates"][j-1]])
    elif(j == 0):
      node.append([i["geometry"]["coordinates"][j+1]])
    else:
      node.append([i["geometry"]["coordinates"][j-1], i["geometry"]["coordinates"][j+1]])

  list_of_nodes.append(node)
  node = {
    "nodes": list_of_nodes
  }

json_data2 = json.dumps(node, indent=4)

with open("nodes.json", "w") as json_file:
  json_file.write(json_data2)