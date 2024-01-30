# app/__init__.py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alerts.db'
app.config.from_object('app.configs.DevelopmentConfig')
api = Api(app)
db = SQLAlchemy(app)

#db.init_app(app)
from app import models, main, email

with app.app_context():
    db.create_all()

