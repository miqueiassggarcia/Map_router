import requests
import json

# Read GeoJSON file
# with open('mapping/data/patos.geojson') as f:
#   data = json.load(f)

# Extract nodes and their coordinates
def get_coordinates_by_road(road):
  Roads = []
  for feature in data['features']:
    if('name' in feature['properties']):
      name = feature['properties']['name']
      if(road in name):
        Roads.append({
          "type": feature["type"],
          "properties": {
            "@id": feature['properties']['@id'],
            "name": name,
            "highway": feature['properties']['highway']
          },
          "geometry": {
            "type": feature["geometry"]["type"],
            "coordinates": feature['geometry']['coordinates']
          }
        })

  path = []
  for road in Roads:
    path.extend(road['geometry']['coordinates'])

  return path[round(len(path) / 2)-1]

url = 'https://viacep.com.br/ws/58704620/json/'

# Faça a solicitação GET para a API
response = requests.get(url)

# Verifique se a solicitação foi bem-sucedida (status code 200)
if response.status_code == 200:
  data = response.json()
  print(data)

  url = f"https://nominatim.openstreetmap.org/search?street={data['logradouro']}&suburb={data['bairro']}&city={data['localidade']}&country=Brasil&format=json"
  print(url)

  # Faça a solicitação GET para a API
  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    print(data)
  else:
    print('Falha na solicitação. Código de status:', response.status_code)
else:
  print('Falha na solicitação. Código de status:', response.status_code)