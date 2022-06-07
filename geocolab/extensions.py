from flask_mail import Mail
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt_manager = JWTManager()
crypt = CryptContext(schemes=['argon2'], deprecated='auto')
ma = Marshmallow()
