import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify
from mapping.finder import find_routes
from flask_cors import CORS
from database.create_database import create_tables
from database.feed_database import populate_tables
from database.process_package import process_express_packages, process_normal_packages

load_dotenv()

app = Flask(__name__)
CORS(app)
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)
cur = connection.cursor()

cur.execute(f"DROP TABLE IF EXISTS endereco CASCADE;")
cur.execute(f"DROP TABLE IF EXISTS entrega CASCADE;")
cur.execute(f"DROP TABLE IF EXISTS remetente CASCADE;")
create_tables(connection)
populate_tables(connection, 10)

@app.route('/populate', methods=['GET'])
def populate():
  populate_tables(connection, 100)
  return jsonify({"message": "success"})

@app.route('/routes_express', methods=['GET'])
def get_route_express():
  results = process_express_packages(connection)
  if not results:
    return jsonify({"message": "failed"})
  else:
    return find_routes(results)

@app.route('/routes_normal', methods=['GET'])
def get_route_normal():
  results = process_normal_packages(connection)
  if not results:
    return jsonify({"message": "failed"})
  else:
    return find_routes(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
