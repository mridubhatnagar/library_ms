from app.extensions import db

import datetime
import uuid
import enum 

from sqlalchemy.types import TypeDecorator, CHAR, Enum
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy import Index



class Members(db.Model):
    member_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    created_at = db.Column(
        DATETIME(fsp=6), default=datetime.datetime.now, nullable=False
    )
    updated_at = db.Column(
        DATETIME(fsp=6),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    