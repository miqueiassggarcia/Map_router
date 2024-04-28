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
      Id SERIAL PRIMARY KEY,
      CEP VARCHAR(8),
      Logradouro VARCHAR(255),
      Municipio VARCHAR(100),
      Estado VARCHAR(50),
      Fragil BOOLEAN,
      Valor DECIMAL(10,2)
  );
  """

  create_delivery_table = """
  CREATE TABLE IF NOT EXISTS Entrega (
      Id SERIAL PRIMARY KEY,
      Nome VARCHAR(100),
      Expresso BOOLEAN,
      Peso DECIMAL(10,2),
      Volume DECIMAL(10,2),
      EnderecoExt INTEGER REFERENCES Endereco(Id),
      RemetenteCPF VARCHAR(11) REFERENCES Remetente(CPF)
  );
  """

  cur.execute(create_address_table)
  cur.execute(create_sender_table)
  cur.execute(create_delivery_table)

  conn.commit()

  cur.close()