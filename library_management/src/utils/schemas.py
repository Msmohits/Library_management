import simplejson
from flask_marshmallow import Marshmallow
from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemySchemaOpts

from .models import db


class FlaskMarshmallowFactory(Marshmallow):

    def __init__(self, *args, **kwargs):
        super(FlaskMarshmallowFactory, self).__init__(*args, **kwargs)


ma = FlaskMarshmallowFactory()


class BaseOpts(SQLAlchemySchemaOpts):
    def __init__(self, meta, ordered=True):
        if not hasattr(meta, 'sql_session'):
            meta.sqla_session = db.session
            meta.json_module = simplejson
            meta.unknown = EXCLUDE
        super(BaseOpts, self).__init__(meta, ordered)


class BaseSchema(SQLAlchemySchema):
    OPTIONS_CLASS = BaseOpts
