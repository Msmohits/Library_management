import simplejson as json
from flask_jwt_extended import JWTManager

from .redis import redis

jwt = JWTManager()


@jwt.user_loader_callback_loader
def my_user_loader_callback_loader(identity):
    if isinstance(identity, str):
        return identity
    user = redis.hmget(identity['id'], 'identity')[0]
    if user:
        return json.loads(user.decode())
    return identity


@jwt.token_in_blacklist_loader
def my_token_is_valid_check(jwt_payload):
    jti = jwt_payload["jti"]
    if redis.get(jti) is not None:
        return True  # token exists in block list for logout users.

    if jwt_payload:
        if 'exp' not in jwt_payload:
            return True
        else:
            rider = jwt_payload['identity']['rider'] if 'identity' in jwt_payload and 'rider' in jwt_payload[
                'identity'] else None
            if rider:
                rider_auth_id = rider['auth_id']
                status = redis.hmget('rider_jwt_auth_id' + str(rider_auth_id), 'status')[0]
                if status:
                    redis.delete(str('rider_jwt_auth_id' + str(rider_auth_id)))
                    return False

            # TODO create password changed list and save id in it. Check the id from identity with the list id.
            pass

    return False
