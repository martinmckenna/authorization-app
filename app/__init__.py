import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_bcrypt import Bcrypt
from app.config import app, DevelopmentConfig, ProductionConfig
from sqlalchemy_utils import create_database, database_exists

config = DevelopmentConfig if os.environ.get(
    'FLASK_ENV') == 'development' else ProductionConfig

app.config.from_object(config)

"""Init app"""
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from app.routes.auth import auth

app.register_blueprint(auth)

if not database_exists(config.URL):
    create_database(config.URL)

has_no_tables = not inspect(db.engine).get_table_names()

if has_no_tables:
    try:
        print('Attempting to create database tables...', flush=True)
        db.create_all()
    except:
        print('Database tables could not be created. - please check to see if they already exist.', flush=True)
