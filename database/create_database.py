def create_tables(conn):
  cur = conn.cursor()

  create_sender_table = """
  CREATE TABLE IF NOT EXISTS Remetente (
    CPF VARCHAR(11) PRIMARY KEY,
    Nome VARCHAR(100)
  );
  """

  create_address_table = """
  CREATE TABLE IF NOT EXISTS Endereco (
    Id VARCHAR(36) PRIMARY KEY,
    Logradouro VARCHAR(255),
    Bairro VARCHAR(100),
    Municipio VARCHAR(100),
    Estado VARCHAR(50)
  );
  """

  create_delivery_table = """
  CREATE TABLE IF NOT EXISTS Entrega (
    Id VARCHAR(36) PRIMARY KEY,
    Nome VARCHAR(120),
    Expresso BOOLEAN,
    Peso DECIMAL(10,2),
    Volume DECIMAL(10,2),
    Fragil BOOLEAN,
    Lucro DECIMAL(10,2),
    Distancia DECIMAL(10,2),
    Tempo TIME,
    Data DATE,
    Prioridade DECIMAL(10, 2),
    Latitude DECIMAL(10, 8),
    Longitude DECIMAL(10, 8),
    EnderecoExt VARCHAR(36) REFERENCES Endereco(Id),
    RemetenteCPF VARCHAR(11) REFERENCES Remetente(CPF)
  );
  """

  cur.execute(create_address_table)
  cur.execute(create_sender_table)
  cur.execute(create_delivery_table)

  conn.commit()

  cur.close()