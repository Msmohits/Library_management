from datetime import datetime

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from src import db, BaseMixin, ReprMixin


class User(BaseMixin, db.Model, ReprMixin):
    id = db.Column(UUID(as_uuid=True), index=True, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = db.Column(db.String(55), nullable=False, index=True)
    email = db.Column(db.String(55), unique=True, nullable=False, index=True)
    mobile_number = db.Column(db.String(10), unique=True, index=True)
    password = db.Column(db.String(255))
    member_joining_date = db.Column(db.DateTime(), default=datetime.utcnow())
    member_valid_till = db.Column(db.DateTime(), default=datetime.utcnow())
    active = db.Column(db.Boolean(), default=False)
    is_admin = db.Column(db.Boolean(), default=False)
    book_status = db.relationship('BooksStatus', uselist=True, back_populates='user', lazy='dynamic')


class Books(BaseMixin, db.Model, ReprMixin):
    __repr_fields__ = ['id']
    id = db.Column(UUID(as_uuid=True), index=True, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = db.Column(db.String(55), unique=True, nullable=False, index=True)
    author = db.Column(db.String(55), unique=True, nullable=False, index=True)
    book_status = db.relationship('BooksStatus', uselist=True, back_populates='books', lazy='dynamic')


class BooksStatus(BaseMixin, db.Model, ReprMixin):
    __repr_fields__ = ['id']

    status = db.Column(db.String(55), unique=False, nullable=True, index=True)
    borrowed_count = db.Column(db.Integer, unique=False, nullable=True, index=True)
    borrow_date = db.Column(db.Date(), default=datetime.utcnow())
    borrow_till = db.Column(db.Date(), default=datetime.utcnow())

    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('books.id'), index=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), index=True, nullable=True)

    user = db.relationship('User', foreign_keys=[user_id], back_populates='book_status')
    books = db.relationship('Books', foreign_keys=[book_id], back_populates='book_status')
