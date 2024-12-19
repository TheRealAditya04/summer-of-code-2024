from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger
from . import db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# Customer Model
class Customer(db.Model):
    __tablename__ = 'customer'

    c_id = db.Column(db.BigInteger, primary_key=True)
    c_name = db.Column(db.String(100), nullable=False)
    c_email = db.Column(db.String(100), nullable=False)
    c_contact = db.Column(db.BigInteger, nullable=False)

    # Relationship with Transaction
    transactions = db.relationship('Transaction', backref='customer')


# Staff Model
class Staff(db.Model):
    __tablename__ = 'staff'

    s_id = db.Column(db.BigInteger, primary_key=True)
    s_name = db.Column(db.String(100), nullable=False)
    s_email = db.Column(db.String(100), nullable=False)
    s_is_admin = db.Column(db.Boolean, default=False)
    s_contact = db.Column(db.BigInteger, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Relationship with Transaction
    transactions = db.relationship('Transaction', backref='staff')


# InventoryItem Model
class InventoryItem(db.Model):
    __tablename__ = 'inventoryitem'

    item_sku = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_name = db.Column(db.String(100), nullable=False)
    item_description = db.Column(db.String(255))
    item_price = db.Column(db.Float, nullable=False)
    item_qty = db.Column(db.Integer, nullable=False)

    # Many-to-Many relationship with Transaction
    transactions = db.relationship(
        'Transaction',
        secondary='transaction_items',
        back_populates='items'
    )


# Association Table for Many-to-Many Relationship
transaction_items = db.Table(
    'transaction_items',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.t_id'), primary_key=True),
    db.Column('item_sku', db.String, db.ForeignKey('inventoryitem.item_sku'), primary_key=True)
)


# Transaction Model
class Transaction(db.Model):
    __tablename__ = 'transaction'

    t_id = db.Column(db.BigInteger, primary_key=True)
    c_id = db.Column(db.BigInteger, db.ForeignKey('customer.c_id'), nullable=False)
    s_id = db.Column(db.BigInteger, db.ForeignKey('staff.s_id'), nullable=False)
    t_date = db.Column(db.DateTime, nullable=False)
    t_amount = db.Column(db.Float, nullable=False)
    t_category = db.Column(db.String(50))

    # Many-to-Many relationship with InventoryItem
    items = db.relationship(
        'InventoryItem',
        secondary='transaction_items',
        back_populates='transactions'
    )
