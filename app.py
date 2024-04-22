from flask import Flask, jsonify
from mapping.finder import find_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
