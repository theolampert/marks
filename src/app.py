from flask import Flask
from config import SECRET_KEY
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = 'cookies'
jwt = JWTManager(app)
