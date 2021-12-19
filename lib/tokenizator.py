import os
import jwt
from datetime import datetime, timedelta
from sanic import Sanic


app = Sanic.get_app(os.environ.get('SANIC_APP_NAME'))
config = app.ctx.config


def create_access_token(data, expires_time):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_time
    to_encode.update({
        'exp': expire,
    })
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm='HS256')


def create_token(user_id: int) -> dict:
    expires_time = timedelta(minutes=3600)
    return {
        'token': create_access_token(
            data={'user_id': user_id},
            expires_time=expires_time
        ),
        'token_type': 'Token'
    }


def decode_token(token: str):
    return jwt.decode(token, config.SECRET_KEY, 'HS256')
