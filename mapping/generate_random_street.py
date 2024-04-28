import json
import random

# Read GeoJSON file
with open('mapping/data/patos.geojson') as f:
  data = json.load(f)

with open('mapping/data/bairrosruaspatos.json') as f:
  data_suburb_street = json.load(f)

def get_street_by_id(id):
  for i in range(len(data["features"])):
    if(data["features"][i]["id"] == "way/" + str(id)):
      if("name" in data["features"][i]["properties"]):
        return data["features"][i]["properties"]["name"]
      else:
        return None
  
  return None

def generate_random_suburb_and_street():
  street = None
  while(street == None):
    random_index = random.randint(0, len(data_suburb_street['elements'])-1)

    suburb = data_suburb_street["elements"][random_index]["tags"]["name"]

    random_index_street = random.randint(0, len(data_suburb_street["elements"][random_index]["members"])-1)
    id_street = data_suburb_street["elements"][random_index]["members"][random_index_street]["ref"]

    street = get_street_by_id(id_street)

  return suburb, street