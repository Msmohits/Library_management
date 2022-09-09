from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy import or_, asc, desc

from .models import User, Books, BooksStatus
from .schemas import UserSchema, BooksSchema, BooksStatusSchema
from ..utils import api, db
from ..utils import security


class UserResource(Resource):
    model = User
    schema = UserSchema

    @jwt_required
    def get(self, slug=None):
        current_user = get_jwt_identity()

        if current_user['is_admin'] and current_user['active']:
            users = User.query
            if slug:
                if '__page' in request.args and request.args.get(
                        '__page') and '__limit' in request.args and request.args.get('__limit'):
                    page = request.args.get('__page')
                    limit = request.args.get('__limit')
                    users = users.limit(limit).offset((int(page) - 1) * int(limit))
                if '__user_name__equal' in request.args and request.args.get('__user_name__equal'):
                    user_name = request.args.get('__user_name__equal')
                    data = self.schema().dump(users.filter(User.name == user_name).all(), many=True)
                    return make_response(jsonify({'User_by_name': data}))
                data = self.schema().dump(users.all(), many=True)
            else:
                data = self.schema().dump(users.order_by(asc(User.name)).all(), many=True)

            return make_response(jsonify({'Users': data}))
        if not current_user['is_admin'] and current_user['active']:
            user = self.model.query.filter(User.id == slug).first()
            data = self.schema().dump(user)
            return make_response(jsonify({'Users': data}), 200)

    def post(self):
        data = request.json
        obj = UserSchema().load(data, session=db.session, many=False)
        db.session.add(obj)
        db.session.commit()
        return 'User Added Successfully', 201

    @jwt_required
    def patch(self, slug):
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            obj = User.query.get(slug)
            data = request.json
            UserSchema().load(data, session=db.session, instance=obj)
            db.session.commit()
            return 'User Updated Successfully', 200
        else:
            return 'You have Permission to do admin work', 403

    @jwt_required
    def delete(self, slug):
        global obj
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            obj = User.query.filter(User.id == slug).first()
        if not current_user['is_admin']:
            obj = User.query.filter(or_(User.id == current_user['id']), (User.id == slug),
                                    (current_user['id'] == slug)).first()
        if not obj:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        db.session.delete(obj)
        db.session.commit()
        return 'User Deleted Successfully', 204


api.add_resource(UserResource, '/user/<slug>', endpoint='user')
api.add_resource(UserResource, '/user', endpoint='user_list')


class BooksResource(Resource):
    model = Books
    schema = BooksSchema

    @jwt_required
    def get(self):
        books = Books.query
        if '__page' in request.args and request.args.get('__page') and '__limit' in request.args and request.args.get(
                '__limit'):
            page = request.args.get('__page')
            limit = request.args.get('__limit')
            books = books.limit(limit).offset((int(page) - 1) * int(limit))
        if '__book_name__equal' in request.args and request.args.get('__book_name__equal'):
            book_name = request.args.get('__book_name__equal')
            data = self.schema().dump(Books.filter(Books.name == book_name).all(), many=True)
            return make_response(jsonify({"book_by_name": data}))
        data = BooksSchema().dump(books.all(), many=True)

        return make_response(jsonify({"books": data}))

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            data = request.json
            obj = BooksSchema().load(data, session=db.session, many=False)
            db.session.add(obj)
            db.session.commit()
            return 'User Added Successfully', 201
        else:
            return 'You have Permission to do admin work', 403

    @jwt_required
    def patch(self, slug):
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            obj = Books.query.get(slug)
            data = request.json
            BooksSchema().load(data, session=db.session, instance=obj)
            db.session.commit()
            return 'User Updated Successfully', 200
        else:
            return 'Permission Denied', 403

    @jwt_required
    def delete(self, slug):
        current_user = get_jwt_identity()
        if current_user['is_admin']:
            obj = self.model.query.get(slug)
            if not obj:
                return make_response(jsonify({'error': 'Resource not found'}), 404)
            db.session.delete(obj)
            db.session.commit()
            return 'Book Deleted Successfully', 204
        else:
            return 'Permission Denied', 403


api.add_resource(BooksResource, '/books/<slug>', endpoint='books')
api.add_resource(BooksResource, '/books', endpoint='books_list')


class BooksStatusResource(Resource):
    model = BooksStatus
    schema = BooksStatusSchema

    @jwt_required
    def get(self):
        books_status = BooksStatus.query
        if '__page' in request.args and request.args.get('__page') and '__limit' in request.args and request.args.get(
                '__limit'):
            page = request.args.get('__page')
            limit = request.args.get('__limit')
            books_status = books_status.limit(limit).offset((int(page) - 1) * int(limit))
        if not books_status:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        data = self.schema().dump(books_status.all(), many=True)
        return make_response(jsonify(data), 200)

    @jwt_required
    def post(self):
        data = request.json
        if data['status'] == 'borrowed' and data['user_id'] and data['book_id']:
            obj = BooksStatusSchema().load(data, session=db.session, many=False)
            db.session.add(obj)
            db.session.commit()
            return 'Book Status Added Successfully', 201

    @jwt_required
    def patch(self, slug):
        data = request.json
        obj = BooksStatus.query.get(slug)
        if data['status'] == 'free':
            self.schema().load(data, session=db.session, instance=obj)
            obj.book_id = None
            obj.user_id = None
            obj.borrow_date = None
            obj.borrow_till = None

            db.session.commit()
            db.session.delete(obj)
            db.session.commit()
            return 'Book Status Updated Successfully', 200


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
