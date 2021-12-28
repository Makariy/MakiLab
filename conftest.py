import pytest
import config
from sanic_testing import TestManager


# Every time when the test runs, initialize an application
@pytest.fixture(scope='session')
def app():
    from src.application import create_app
    app = create_app(config)
    TestManager(app)
    return app



