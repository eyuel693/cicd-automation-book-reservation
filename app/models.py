# app/models.py
from . import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    reserved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Book {self.title}>'