import json

with open('nodes.json') as f:
  nodes = json.load(f)

wrong = 0
right = 0
for node in nodes:
  verified = False
  for i in range(0, len(node["connections"])):
    for verificacao in nodes:
      if(node["connections"][i]["id"] == verificacao["id"]):
        verified = True
  if(verified == False):
    wrong = wrong + 1
  else:
    right = right + 1

print(wrong)
print(right)