import requests
import json

def add_leading_zeros(number):    
  string_number = str(number)
  
  return '5870' + '0' * (4 - len(string_number)) + string_number

ceps = {}
for i in range(100):
  url = f'https://viacep.com.br/ws/{add_leading_zeros(i)}/json/'

  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    if("erro" not in data):
      ceps[data['cep']] = data


with open("data/ceps.json", "w") as json_file:
  json.dump(ceps, json_file, indent=4, ensure_ascii=False)