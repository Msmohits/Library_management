import base64
import binascii
import hashlib
import hmac

from flask_jwt_extended import create_access_token, create_refresh_token

from ..books import models, schemas
from ..utils import db


def get_hmac(password):
    return base64.b64encode(hmac.new('test'.encode('utf-8'), password.encode('utf-8'),
                                     hashlib.sha512).digest()).decode('ascii')


class FlaskSecurity(object):

    def __init__(self, app=None, data_store=None):
        self.app = app
        self.data_store = data_store

        if app is not None and data_store is not None:
            self.init_app(app, data_store)

    def init_app(self, app, data_store=None):
        self.app = app
        if data_store:
            self.data_store = data_store
        return

    def get_user(self, email: str = None, mobile_number: str = None, model=None) -> str:
        if email:
            kk = self.data_store.query.with_entities(self.data_store.id) \
                .filter(self.data_store.email == email, self.data_store.active.isnot(False)) \
                .limit(1).scalar()
            return self.data_store.query.with_entities(self.data_store.id) \
                .filter(self.data_store.email == email, self.data_store.active.isnot(False)) \
                .limit(1).scalar()
        else:
            return self.data_store.query.with_entities(self.data_store.id) \
                .filter(model.mobile_number == mobile_number, self.data_store.active.isnot(False)) \
                .limit(1).scalar()

    def check_password(self, id, verify_password) -> bool:
        password = self.data_store.query.with_entities(self.data_store.password) \
            .filter(self.data_store.id == id).limit(1).scalar()
        try:
            if len(base64.b64decode(password).hex()):
                password = get_hmac(verify_password)
                return password == get_hmac(verify_password)
            else:
                raise binascii.Error
        except binascii.Error as e:
            print(e)
            new_password = get_hmac(password)
            self.data_store.query \
                .filter(self.data_store.id == id).update({'password': new_password})
            db.session.commit()
            return password == verify_password

    def get_token(self, id):
        global user_id
        identity = schemas.UserSchema().dump(self.data_store.query.get(id))
        user_id = identity['id']

        return create_access_token(identity=identity, ), create_refresh_token(identity=user_id)


security = FlaskSecurity(data_store=models.User)
