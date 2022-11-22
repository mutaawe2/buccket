from flask import Flask 
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api 
from flask_jwt_extended import JWTManager

convention = {
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
}

metadata = MetaData(naming_convention=convention)

api = Api()
migrate = Migrate()
cors = CORS()
mail = Mail()
db = SQLAlchemy(metadata=metadata)
jwt = JWTManager()
ma = Marshmallow()
Login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    Login_manager.init_app(app)
    
    
     # jwt headers required 
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user['id']
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from bucketList.models import User
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()
    
        
    return app

from .auth import auth_routes
from .bk_list import bucket_routes
from .user import user_routes

auth_routes(api)
bucket_routes(api)
user_routes(api)

