import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify
from mapping.finder import find_routes
from flask_cors import CORS
from database.create_database import create_tables
from database.feed_database import populate_tables

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
populate_tables(connection, 100)

# Route to get all books
@app.route('/routes', methods=['GET'])
def get_route():
  return jsonify(find_routes())

# # Route to get a specific book by id
# @app.route('/books/<int:book_id>', methods=['GET'])
# def get_book(book_id):
#   book = next((book for book in books if book['id'] == book_id), None)
#   if book:
#       return jsonify(book)
#   else:
#       return jsonify({"message": "Book not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
