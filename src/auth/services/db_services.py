from typing import Union, Tuple

from lib.models import User
from tortoise.exceptions import DoesNotExist


async def get_user_by_params(**kwargs) -> Union[User, None]:
    try:
        return await User.get(**kwargs)
    except DoesNotExist:
        return None


async def create_user(username: str, password: str) -> Tuple[User, Union[str, None]]:
    return await User.create_user(username=username, password=password), None


