import os
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

USER = os.getenv("MYSQL_USER")
PASS = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
DB_NAME = os.getenv("MYSQL_DB")


class BaseConfig:
    """Base configuration."""
    app.config['MYSQL_DATABASE_USER'] = USER
    app.config['MYSQL_DATABASE_PASSWORD'] = PASS
    app.config['MYSQL_DATABASE_HOST'] = HOST
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")


class ProductionConfig(BaseConfig):
    """Production configuration."""
    app.config['MYSQL_DATABASE_DB'] = DB_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}:3306/{DB_NAME}'
    URL = f'mysql+pymysql://{USER}:{PASS}@{HOST}:3306/{DB_NAME}'


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    app.config['MYSQL_DATABASE_DB'] = DB_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASS}@{HOST}:3306/{DB_NAME}'
    URL = f'mysql+pymysql://{USER}:{PASS}@{HOST}:3306/{DB_NAME}'
