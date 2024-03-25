from app.extensions import db

import datetime
import uuid
import enum 

from sqlalchemy.types import TypeDecorator, CHAR, Enum
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy import Index



class Books(db.Model):
    id = db.Column(db.Integer(), nullable=False, autoincrement=True, primary_key=True)
    bookID = db.Column(db.Integer(), nullable=False, unique=True)
    title = db.Column(db.String(250), nullable=False)
    created_at = db.Column(
        DATETIME(fsp=6), default=datetime.datetime.now, nullable=False
    )
    updated_at = db.Column(
        DATETIME(fsp=6),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )
    authors = db.Column(db.String(100), nullable=False)
    average_rating = db.Column(db.Float())
    isbn = db.Column(db.String(20), nullable=False)
    isbn13 = db.Column(db.String(20), nullable=False)
    num_pages = db.Column(db.Integer())
    rating_count = db.Column(db.Integer())
    text_reviews_count = db.Column(db.Integer())
    publication_date = db.Column(db.String(20))
    publisher = db.Column(db.String(20))
    language_code = db.Column(db.String(10))
    stock = db.Column(db.Integer(), default="5")
    books_available = db.Column(db.Integer(), default="5")

