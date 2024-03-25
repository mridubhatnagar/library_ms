from app.extensions import db

import datetime
import uuid
import enum 

from sqlalchemy.types import TypeDecorator, CHAR, Enum
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy import Index



class Transactions(db.Model):
    id = db.Column(db.Integer(), nullable=False, autoincrement=True, primary_key=True)
    member_id = db.Column(db.Integer(), db.ForeignKey("members.member_id"), nullable=False)
    book_id = db.Column(db.Integer(), db.ForeignKey("books.bookID"), nullable=False)
    created_at = db.Column(
        DATETIME(fsp=6), default=datetime.datetime.now, nullable=False
    )
    updated_at = db.Column(
        DATETIME(fsp=6),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )
    book_issued_date = db.Column(
        DATETIME(fsp=6), default=datetime.datetime.today().date(), nullable=False
    )
    book_returned_date = db.Column(
        DATETIME(fsp=6), nullable=True
    )
