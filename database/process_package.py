import time
from dotenv import load_dotenv

load_dotenv()

def process_db_response(packages):
  sequence_of_packages = []
  total_weight = packages[0][3]
  total_volume = packages[0][4]

  i = 0
  if(len(packages) > 1):
    print(len(packages))
    # while(total_weight + packages[i+1][3] <= 400 and (total_volume + packages[i+1][4]) <= 10 and i < len(packages)):
    while(i < len(packages)):
      print(i)
      sequence_of_packages.append({
        "coordinate": (float(packages[i][12]), float(packages[i][11])),
        "package": {
          "id": packages[i][0],
          "name": packages[i][1],
          "expresso": packages[i][2],
          "peso": float(packages[i][3]),
          "volume": float(packages[i][4]),
          "fragil": packages[i][5],
          "time": packages[i][8],
          "data": packages[i][9]
        },
        "sender": {
          "cpf": packages[i][16],
          "name": packages[i][15]
        },
        "address": {
          "street": packages[i][17],
          "suburb": packages[i][18],
          "city": packages[i][19],
          "state": packages[i][20]
        }
      })

      total_weight += packages[i][3]
      total_volume += packages[i][4]
      i += 1
  else:
    sequence_of_packages.append({
      "coordinate": (float(packages[i][12]), float(packages[i][11])),
      "package": {
        "id": packages[i][0],
        "name": packages[i][1],
        "expresso": packages[i][2],
        "peso": float(packages[i][3]),
        "volume": float(packages[i][4]),
        "fragil": packages[i][5],
        "time": packages[i][8],
        "data": packages[i][9]
      },
      "sender": {
        "cpf": packages[i][16],
        "name": packages[i][15]
      },
      "address": {
        "street": packages[i][17],
        "suburb": packages[i][18],
        "city": packages[i][19],
        "state": packages[i][20]
      }
    })
  
  return sequence_of_packages

def process_express_packages(connection):
  cur = connection.cursor()

  while True:
    cur.execute("""
      SELECT 
        Entrega.Id AS EntregaId,
        Entrega.Nome AS NomeEntrega,
        Entrega.Expresso,
        Entrega.Peso,
        Entrega.Volume,
        Entrega.Fragil,
        Entrega.Lucro,
        Entrega.Distancia,
        Entrega.Tempo,
        Entrega.Data,
        Entrega.Prioridade,
        Entrega.Latitude,
        Entrega.Longitude,
        Entrega.EnderecoExt,
        Entrega.RemetenteCPF,
        Remetente.Nome AS NomeRemetente,
        Remetente.CPF AS CPFRemetente,
        Endereco.Logradouro,
        Endereco.Bairro,
        Endereco.Municipio,
        Endereco.Estado
      FROM 
        Entrega
      JOIN 
        Remetente ON Entrega.RemetenteCPF = Remetente.CPF
      JOIN 
        Endereco ON Entrega.EnderecoExt = Endereco.Id
      WHERE 
        Entrega.Expresso = TRUE
      ORDER BY 
        Entrega.Prioridade DESC
      LIMIT 100;
    """)
    if cur.rowcount > 0:
      break
    time.sleep(1)
  
  expresso_packages = cur.fetchall()

  return process_db_response(expresso_packages)
# AND (
#   SELECT SUM(Volume) FROM Entrega WHERE Entrega.Expresso = TRUE
# ) <= 4
# AND (
#   SELECT SUM(Peso) FROM Entrega WHERE Entrega.Expresso = TRUE
# ) <= 500

def process_normal_packages(connection):
  cur = connection.cursor()

  while True:
    cur.execute("""
      SELECT 
        Entrega.Id AS EntregaId,
        Entrega.Nome AS NomeEntrega,
        Entrega.Expresso,
        Entrega.Peso,
        Entrega.Volume,
        Entrega.Fragil,
        Entrega.Lucro,
        Entrega.Distancia,
        Entrega.Tempo,
        Entrega.Data,
        Entrega.Prioridade,
        Entrega.Latitude,
        Entrega.Longitude,
        Entrega.EnderecoExt,
        Entrega.RemetenteCPF,
        Remetente.Nome AS NomeRemetente,
        Remetente.CPF AS CPFRemetente,
        Endereco.Logradouro,
        Endereco.Bairro,
        Endereco.Municipio,
        Endereco.Estado
      FROM 
        Entrega
      JOIN 
        Remetente ON Entrega.RemetenteCPF = Remetente.CPF
      JOIN 
        Endereco ON Entrega.EnderecoExt = Endereco.Id
      WHERE 
        Entrega.Expresso = FALSE
      ORDER BY 
        Entrega.Prioridade DESC
      LIMIT 100;
    """)
    if cur.rowcount > 0:
      break
    time.sleep(1)
  
  expresso_packages = cur.fetchall()

  return process_db_response(expresso_packages)
# AND (
#   SELECT SUM(Volume) FROM Entrega WHERE Entrega.Expresso = TRUE
# ) <= 4
# AND (
#   SELECT SUM(Peso) FROM Entrega WHERE Entrega.Expresso = TRUE
# ) <= 500