import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(url)
cur = conn.cursor()

cur.execute("""
  SELECT * FROM Entrega
  WHERE Expresso = TRUE
  ORDER BY Data
""")

expresso_packages = cur.fetchall()

for package in expresso_packages:
    print(package)

cur.close()
conn.close()