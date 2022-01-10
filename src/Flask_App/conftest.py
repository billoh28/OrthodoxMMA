import pytest
import sys, os

from app import create_app, load_configs

# Give each test the same app to test
app_context, ip =  create_app()

print(os.getcwd())

# Load configs
app_context = load_configs(app_context)

# These fixtures are ran before tests and set up the environment for tests e.g. variables 

# App instance the tests can call (tests call the name of the function as the variable returned by the function)
@pytest.fixture
def app():
    yield app_context

# Tests use this client to make requests instead of starting the server
@pytest.fixture
def client(app):
    # Make test device here
    app.config['SECRET_KEY'] = 'sekrit!'
    app.config['TESTING'] = True
    return app.test_client()
