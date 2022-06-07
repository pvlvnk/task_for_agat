from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()


class Author(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    first_name = db.Column(
        db.String(50),
        nullable=False
    )
    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def update(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class AuthorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name')


class Book(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('author.id'),
        nullable=False
    )
    author = db.relationship(
        'Author',
        backref=db.backref('books', lazy='dynamic')
    )

    def __init__(self, title, author_id):
        self.title = title
        self.author_id = author_id

    def update(self, title, author_id):
        self.title = title
        self.author_id = author_id


class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author_id')
