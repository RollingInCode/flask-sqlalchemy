from flask import Flask, request, jsonify
from peewee import *
from flask_peewee.db import Database

app = Flask(__name__)
app.config['DATABASE'] = {
    'name': 'books.db',
    'engine': 'peewee.SqliteDatabase',
}
db = Database(app)

class Book(db.Model):
    title = CharField()
    author = CharField()

@app.route('/book', methods=['POST'])
def create_book():
    data = request.get_json()
    book = Book.create(title=data['title'], author=data['author'])
    return jsonify({"message": f"Book '{book.title}' by {book.author} created successfully."})

@app.route('/book', methods=['GET'])
def get_books():
    books = Book.select()
    return jsonify({"books": [{"id": book.id, "title": book.title, "author": book.author} for book in books]})

@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.get(Book.id == id)
    if book:
        return jsonify({"book": {"id": book.id, "title": book.title, "author": book.author}})
    else:
        return jsonify({"error": "Book not found"}), 404

@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    query = Book.update(title=data['title'], author=data['author']).where(Book.id == id)
    if query.execute():
        return jsonify({"message": f"Book updated successfully."})
    else:
        return jsonify({"error": "Book not found"}), 404

@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    query = Book.delete().where(Book.id == id)
    if query.execute():
        return jsonify({"message": f"Book deleted successfully."})
    else:
        return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    db.database.create_tables([Book])
    app.run(debug=True)
