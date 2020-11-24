from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from app.config import app, DevelopmentConfig, ProductionConfig
from sqlalchemy_utils import create_database, database_exists

config = DevelopmentConfig if os.environ.get('FLASK_ENV') == 'development' else ProductionConfig
    
if not database_exists(config.URL): 
  create_database(config.URL)

app.config.from_object(config)

"""Init app"""
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

