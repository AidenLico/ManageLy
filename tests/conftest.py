import sys
import os

# Add the root directory to the Python path so that 'app' module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app as flaskApp

@pytest.fixture
def app():
    flaskApp.config.update({
        "TESTING": True,
        "SECRET_KEY": "test"
    })
    return flaskApp

@pytest.fixture
def client(app):
    return app.test_client()