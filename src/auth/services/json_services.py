from typing import Dict
from auth.models import User


def render_user(user: User) -> Dict[str, Dict[str, str]]:
    return {
        'user': {
            'username': user.username,
            'uuid': str(user.uuid)
        }
    }

