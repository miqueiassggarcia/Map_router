import json
import requests

with open("data/ceps.json", "r", encoding="utf-8") as json_file:
    ceps = json.load(json_file)

def get_coordenadas_por_endereco(rua, bairro):
    rua = rua.replace(" ", "%20")
    bairro = bairro.replace(" ", "%20")
    
    url = f'https://nominatim.openstreetmap.org/search?street={rua}&suburb={bairro}&city=Patos&country=Brasil&format=json'
    
    print(url)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data:
            return {
                'latitude': float(data[0]['lat']),
                'longitude': float(data[0]['lon'])
            }
        else:
            print("Endereço não encontrado.")
            return None
    else:
        print(response)
        print('Falha na solicitação. Código de status:', response.status_code)
        return None

for value in ceps.values():
    rua = value['logradouro']
    bairro = value['bairro']

    coordenadas = get_coordenadas_por_endereco("Rua Bossuet Wanderley", "Centro")
    if coordenadas:
        print("Coordenadas de", rua + ",", bairro + ":", coordenadas)
    else:
        print("Não foi possível obter as coordenadas do endereço.")
