from typing import Dict, Literal
from auth.models import User


async def render_user(user: User) -> Dict[Literal['user'], Dict[str, str]]:
    return {
        'user': {
            'username': user.username,
            'uuid': str(user.uuid)
        }
    }

