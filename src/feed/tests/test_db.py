from sanic import Sanic  # type: Ignore
import pytest
from lib.models import User
from lib.tests import require_database


@pytest.mark.asyncio
@require_database
async def test_user_creation(app: Sanic):
    username = 'Makar'

    user = await User.create_user(username, 'Kariy123')
    assert user.id is not None
    assert user.username == username


