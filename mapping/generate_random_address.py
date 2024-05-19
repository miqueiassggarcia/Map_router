import json
import random

with open("mapping/data/ceps.json", "r", encoding="utf-8") as json_file:
  ceps = json.load(json_file)

def generate_random_address():
  random_cep = random.choice(list(ceps.keys()))
  return {"cep": random_cep, **ceps[random_cep]}