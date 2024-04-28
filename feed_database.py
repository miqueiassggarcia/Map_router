import random
import psycopg2

# Function to generate random CPF number
def generate_cpf():
  return ''.join([str(random.randint(0, 9)) for _ in range(11)])

# Function to generate random name
def generate_name():
  names = ["John", "Jane", "Alice", "Bob", "Michael", "Emma", "David", "Sarah"]
  return random.choice(names)

# Function to generate random delivery details
def generate_delivery():
  names = ["Package A", "Package B", "Package C", "Package D", "Package E"]
  expresso = random.choice([True, False])
  peso = round(random.uniform(0.1, 10.0), 2)
  volume = round(random.uniform(0.1, 5.0), 2)
  return {
    "Nome": random.choice(names),
    "Expresso": expresso,
    "Peso": peso,
    "Volume": volume
  }

# Function to populate the tables with random data
def populate_tables(conn, num_records):
  cur = conn.cursor()

  # Populate Remetente table
  for _ in range(num_records):
    cpf = generate_cpf()
    nome = generate_name()
    cur.execute("INSERT INTO Remetente (CPF, Nome) VALUES (%s, %s)", (cpf, nome))

  # Populate Entrega table
  for _ in range(num_records):
    delivery = generate_delivery()
    remetente_cpf = generate_cpf()
    cur.execute("""
      INSERT INTO Entrega (Nome, Expresso, Peso, Volume, RemetenteCPF) 
      VALUES (%s, %s, %s, %s, %s)
    """, (delivery['Nome'], delivery['Expresso'], delivery['Peso'], delivery['Volume'], remetente_cpf))

  conn.commit()
  cur.close()