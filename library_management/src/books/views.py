import jwt
from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required, current_user, decode_token, get_jwt_identity
from flask_restful import Resource
from .models import User, Books, BooksStatus
from .schemas import UserSchema, BooksSchema, BooksStatusSchema
from ..utils import api, db
from ..utils import security
from sqlalchemy import and_, func, desc, or_, asc



class UserResource(Resource):
    model = User
    schema = UserSchema

    @jwt_required
    def get(self, slug):

        print(current_user['is_admin'])
        user = self.model.query.filter(User.id == slug).first()
        if user and user.is_admin and user.active:
            users = User.query.all()
            print(users)
            data = self.schema().dump(users, many=True)
            print(data)
            return make_response(jsonify({'Users': data}))
        if user and user is not user.is_admin and user.active:
            data = self.schema().dump(user)
            return make_response(jsonify({'Users': data}),200)

    def post(self):
        data = request.json
        obj = UserSchema().load(data, session=db.session, many=False)
        db.session.add(obj)
        db.session.commit()
        return 'User Added Successfully',201

    @jwt_required
    def patch(self, slug):
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            obj = User.query.get(slug)
            data = request.json
            UserSchema().load(data, session=db.session, instance=obj)
            db.session.commit()
            return 'User Updated Successfully',200

    @jwt_required
    def delete(self, slug):
        global obj
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            obj = User.query.filter(User.id == slug).first()
        if not current_user['is_admin']:
            obj = User.query.filter(or_(User.id == current_user['id'] ), (User.id == slug), (current_user['id'] == slug)).first()
        if not obj:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        db.session.delete(obj)
        db.session.commit()
        return make_response(jsonify({}), 204)


api.add_resource(UserResource, '/user/<slug>', endpoint='user')
api.add_resource(UserResource, '/user', endpoint='user_list')


class BooksResource(Resource):
    model = Books
    schema = BooksSchema

    def get(self, slug=None):
        if slug:
            books = Books.query.get(slug)
            type = False
        else:
            books = Books.query.all()
            type = True

        data = BooksSchema().dump(books, many=type)
        print(data)

        return make_response(jsonify({"book": data}))

    def post(self):
        data = request.json
        obj = BooksSchema().load(data, session=db.session, many=False)
        db.session.add(obj)
        db.session.commit()
        return 'User Added Successfully',201

    def patch(self, slug):
        obj = Books.query.get(slug)
        data = request.json
        BooksSchema().load(data, session=db.session, instance=obj)

        db.session.commit()
        return 'User Updated Successfully',200

    def delete(self, slug):
        obj = self.model.query.get(slug)
        if not obj:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        db.session.delete(obj)
        db.session.commit()
        return make_response(jsonify('success'), 204)


api.add_resource(BooksResource, '/books/<slug>', endpoint='books')
api.add_resource(BooksResource, '/books', endpoint='books_list')


class BooksStatusResource(Resource):
    model = BooksStatus
    schema = BooksStatusSchema

    def get(self):
        books_status = BooksStatus.query.all()
        if not books_status:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        data = self.schema().dump(books_status, many=True)
        return make_response(jsonify(data), 200)

    def post(self):
        data = request.json
        if data['status'] == 'borrowed' and data['user_id'] and data['book_id']:
            obj = BooksStatusSchema().load(data, session=db.session, many=False)
            db.session.add(obj)
            db.session.commit()
            return 'Book Status Added Successfully',201


    def patch(self, slug):
        data = request.json
        obj = BooksStatus.query.get(slug)
        data = request.json
        if data['status'] == 'free':
            self.schema().load(data, session=db.session, instance=obj)
            obj.book_id = None
            obj.user_id = None

            db.session.commit()
            db.session.delete(obj)
            db.session.commit()
            return 'User Updated Successfully',200


    def delete(self, slug):
        obj = self.model.query.get(slug)
        if not obj:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        db.session.delete(obj)
        db.session.commit()
        return make_response(jsonify({}), 204)


api.add_resource(BooksStatusResource, '/book_status/<slug>', endpoint='book_status')
api.add_resource(BooksStatusResource, '/book_status', endpoint='book_status_list')


class LoginResource(Resource):
    model = User
    schema = UserSchema

    def post(self):
        data = request.json
        user_id = security.security.get_user(email=data['email'])

        if not user_id:
            return make_response(jsonify({'message': 'User not found'}), 403)

        verified = security.security.check_password(user_id, data['password'])
        if not verified:
            return make_response(jsonify({'message': 'Invalid password'}), 403)
        access_token, refresh_token = security.security.get_token(user_id)
        return make_response(
            jsonify({'token': 'Bearer ' + access_token,
                     'refresh_token': 'Bearer ' + refresh_token}), 200)


api.add_resource(LoginResource, '/login', endpoint='login')
