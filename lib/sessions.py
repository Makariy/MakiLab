from lib.models import User
from lib.services import get_user_by_params
from lib.tokenizator import create_token, decode_token


class SessionCreator:
    @staticmethod
    async def create_session(user: User):
        token = create_token(user.id)
        return token['token']

    @staticmethod
    async def get_user_by_token(token):
        user_id = decode_token(token)['user_id']
        return await get_user_by_params(id=user_id)
