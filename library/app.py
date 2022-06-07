from flask import Flask, jsonify, request
from flask_migrate import Migrate

from models import (Author, AuthorSchema, Book, BookSchema, db,
                    ma)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route('/author/', methods=('GET', 'POST'))
def get_or_create_authors():
    if request.method == 'GET':
        authors = Author.query.all()
        return jsonify(authors_schema.dump(authors)), 200
    else:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        new_author = Author(first_name, last_name)

        db.session.add(new_author)
        db.session.commit()
        return author_schema.jsonify(new_author), 201


@app.route('/author/<id>', methods=('GET', 'PUT', 'DELETE'))
def get_or_update_or_delete_author(id):
    author = Author.query.get(id)
    if request.method == 'GET':
        return author_schema.jsonify(author)
    elif request.method == 'PUT':
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        author.update(first_name, last_name)

        db.session.commit()
        return author_schema.jsonify(author), 200
    else:
        db.session.delete(author)
        db.session.commit()
        return author_schema.jsonify(author), 204


@app.route('/book/', methods=('GET', 'POST'))
def get_books():
    if request.method == 'GET':
        books = Book.query.all()
        return jsonify(books_schema.dump(books))
    else:
        title = request.json['title']
        author_id = request.json['author_id']
        new_book = Book(title, author_id)

        db.session.add(new_book)
        db.session.commit()
        return book_schema.jsonify(new_book), 201


@app.route('/book/<id>', methods=('GET', 'PUT', 'DELETE'))
def book_detail(id):
    book = Book.query.get(id)
    if request.method == 'GET':
        return book_schema.jsonify(book)
    elif request.method == 'PUT':
        title = request.json['title']
        author_id = request.json['author_id']
        book.update(title, author_id)

        db.session.commit()
        return book_schema.jsonify(book), 200
    else:
        db.session.delete(book)
        db.session.commit()
        return book_schema.jsonify(book), 204


@app.route('/book/author=<author_id>', methods=('GET',))
def get_book_from_author(author_id):
    author = Author.query.get(author_id)
    return books_schema.jsonify(author.books.all()), 200


if __name__ == '__main__':
    app.run(debug=False)
