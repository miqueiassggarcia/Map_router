from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="route_master")

def get_coordenadas_por_endereco(rua, bairro):
  endereco = f"{rua}, {bairro}, Patos, BR"

  try:    
    location = geolocator.geocode(endereco)
    
    if location:
      return location.latitude, location.longitude
    else:
      print("Endereço não encontrado.")
      return None, None
  except Exception as e:
    print(e)