from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr.models import db, Customer, Staff, InventoryItem, Transaction

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:winterdsoc@localhost/myproject'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app
