import random
from mapping.generate_random_street import generate_random_suburb_and_street
import uuid
from datetime import timedelta, datetime
from mapping.get_road import get_coordinates_by_road
from mapping.dijkstra import dijkstra
from mapping.process import graph

# Function to generate random CPF number
def generate_cpf():
  return ''.join([str(random.randint(0, 9)) for _ in range(11)])

# Function to generate random name
def generate_name():
  first_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack", "Katie", "Liam", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rose", "Sam", "Tara"]

  last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "White"]

  return random.choice(first_names) + " " + random.choice(last_names)

def calculate_time_by_distance(distance, speed):
  time = distance / speed
  return time

def format_minutes(decimal_minutes):
  total_seconds = int(decimal_minutes * 60)
  
  timedelta_object = timedelta(seconds=total_seconds)
  base_time = datetime(1900, 1, 1) + timedelta_object
  
  formatted_time = base_time.strftime('%H:%M:%S')
  return formatted_time

# Function to generate random delivery details
def generate_delivery(rua):
  names = [f"Package {chr(ord('A') + i)}" for i in range(26)]
  expresso = random.choices(population=[False, True], weights=[0.7, 0.3], k=1)
  fragil = random.choices(population=[False, True], weights=[0.6, 0.4], k=1)
  peso = round(random.uniform(0.1, 10.0), 2)
  volume = round(random.uniform(0.1, 5.0), 2)
  lucro = round(random.uniform(10.0, 150.0), 2)
  data = datetime.now() + timedelta(days=random.randint(1, 30))
  coordinates_of_road = get_coordinates_by_road(rua)
  path, distance = dijkstra(graph, tuple(coordinates_of_road), (-37.2888462, -7.0266789))
  time_estimated = calculate_time_by_distance(distance * 250, 60) * 60
  time_formated = format_minutes(time_estimated)

  return {
    "Nome": random.choice(names),
    "Expresso": expresso[0],
    "Peso": peso,
    "Volume": volume,
    "Fragil": fragil[0],
    "Lucro": lucro,
    "Data": data,
    "Distancia": distance * 250,
    "Tempo": time_formated
  }

# Function to populate the tables with random data
def populate_tables(conn, num_records):
  cur = conn.cursor()

  municipio = "Patos"
  estado = "PB"
  # Populate Remetente table
  for _ in range(num_records):
    cpf = generate_cpf()
    nome = generate_name()
    cur.execute("INSERT INTO Remetente (CPF, Nome) VALUES (%s, %s)", (cpf, nome))

    endereco_id = str(uuid.uuid4())
    bairro, rua = generate_random_suburb_and_street()
    cur.execute("""
      INSERT INTO Endereco (Id, Logradouro, Bairro, Municipio, Estado) 
      VALUES (%s, %s, %s, %s, %s)
      """, (
        endereco_id,
        rua,
        bairro,
        municipio,
        estado
      )
    )

    entrega_id = str(uuid.uuid4())
    delivery = generate_delivery(rua)
    cur.execute("""
      INSERT INTO Entrega (Id, Nome, Expresso, Peso, Volume, Fragil, Lucro, Distancia, Tempo, Data, EnderecoExt, RemetenteCPF) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
      """, (
        entrega_id,
        delivery['Nome'],
        delivery['Expresso'],
        delivery['Peso'],
        delivery['Volume'],
        delivery['Fragil'],
        delivery['Lucro'],
        delivery['Distancia'],
        delivery['Tempo'],
        delivery['Data'],
        endereco_id,
        cpf
      )
    )


  conn.commit()
  cur.close()