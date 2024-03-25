from app.extensions import db

import datetime
import uuid
import enum 

from sqlalchemy.types import TypeDecorator, CHAR, Enum
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy import Index


class Payments(db.Model):
    id = db.Column(db.Integer(), nullable=False, autoincrement=True, primary_key=True)
    member_id = db.Column(db.Integer(), db.ForeignKey("members.member_id"), nullable=False)
    transaction_id = db.Column(db.Integer(), db.ForeignKey("transactions.id"))
    created_at = db.Column(
        DATETIME(fsp=6), default=datetime.datetime.now, nullable=False
    )
    updated_at = db.Column(
        DATETIME(fsp=6),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )
    amount_due = db.Column(db.Integer(), nullable=False, default=0)
    amount_paid = db.Column(db.Integer(), nullable=False, default=0)
    

