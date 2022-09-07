from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src import ma

from .models import User, BooksStatus, Books


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        # exclude = ('book_status',)

    id = ma.UUID(load=True)
    name = ma.String(load=True, allow_none=False)
    email = ma.String(load=True, allow_none=True)
    mobile_number = ma.String(load=True, allow_none=True)
    password = ma.String(load=True, allow_none=True)
    member_joining_date = ma.String(load=True, dump=True)
    member_valid_till = ma.String(load=True, dump=True)
    active = ma.Boolean(load=True)
    is_admin = ma.Boolean(load=True)
    book_status = ma.Nested('BooksStatusSchema', load=True, allow_none=True, many=True,
                            only=('id', 'status', 'borrow_date', 'borrow_till'))


class BooksSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Books
        include_relationships = True
        load_instance = True
        # exclude = ('book_status',)

    id = ma.UUID(load=True)
    name = ma.String(load=True, allow_none=False)
    author = ma.String(load=True, allow_none=False)
    book_status = ma.Nested('BooksStatusSchema', load=True, allow_none=True, many=True,
                            only=('id', 'status', 'borrow_date', 'borrow_till'))


class BooksStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BooksStatus
        include_relationships = True
        load_instance = True
        # exclude = ('user',)

    id = ma.UUID(load=True)

    status = ma.String(load=True, allow_none=False)
    book_id = ma.UUID(load=True, allow_none=True)
    user_id = ma.UUID(load=True, allw_none=True)
    borrow_date = ma.String(load=True)
    borrow_till = ma.String(load=True)
    user = ma.Nested('UserSchema', load=True, allow_none=True, many=False,
                     only=('id', 'name', 'mobile_number', 'email'))
    books = ma.Nested('BooksSchema', load=True, allow_none=True, many=False, only=('id', 'name', 'author'))
