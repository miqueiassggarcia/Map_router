import requests

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