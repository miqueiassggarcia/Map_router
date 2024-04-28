import random
from mapping.generate_random_street import generate_random_suburb_and_street
import uuid

# Function to generate random CPF number
def generate_cpf():
  return ''.join([str(random.randint(0, 9)) for _ in range(11)])

# Function to generate random name
def generate_name():
  first_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack", "Katie", "Liam", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rose", "Sam", "Tara"]

  last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "White"]

  return random.choice(first_names) + " " + random.choice(last_names)

# Function to generate random delivery details
def generate_delivery():
  names = ["Package A", "Package B", "Package C", "Package D", "Package E"]
  expresso = random.choices(population=[False, True], weights=[0.7, 0.3], k=1)
  fragil = random.choices(population=[False, True], weights=[0.6, 0.4], k=1)
  peso = round(random.uniform(0.1, 10.0), 2)
  volume = round(random.uniform(0.1, 5.0), 2)
  valor = round(random.uniform(10.0, 150.0), 2)
  return {
    "Nome": random.choice(names),
    "Expresso": expresso[0],
    "Peso": peso,
    "Volume": volume,
    "Fragil": fragil[0],
    "Valor": valor
  }

# Function to populate the tables with random data
def populate_tables(conn, num_records):
  cur = conn.cursor()

  # Populate Remetente table
  for _ in range(num_records):
    cpf = generate_cpf()
    nome = generate_name()
    cur.execute("INSERT INTO Remetente (CPF, Nome) VALUES (%s, %s)", (cpf, nome))

    endereco_id = str(uuid.uuid4())
    bairro, rua = generate_random_suburb_and_street()
    municipio = "Patos"
    estado = "PB"
    cur.execute("""
      INSERT INTO Endereco (Id, Logradouro, Bairro, Municipio, Estado) 
      VALUES (%s, %s, %s, %s, %s)
    """, (endereco_id, rua, bairro, municipio, estado))

    entrega_id = str(uuid.uuid4())
    delivery = generate_delivery()
    cur.execute("""
      INSERT INTO Entrega (Id, Nome, Expresso, Peso, Volume, Fragil, Valor, EnderecoExt, RemetenteCPF) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (entrega_id, delivery['Nome'], delivery['Expresso'], delivery['Peso'], delivery['Volume'], delivery['Fragil'], delivery['Valor'], endereco_id, cpf))


  conn.commit()
  cur.close()