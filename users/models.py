import config as config

from carts.models import carts
from orders.models import orders

db=config.db


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    salt = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(15), nullable=True)
    contact = db.Column(db.String(12), nullable=True)
    activation_code = db.Column(db.String(20), nullable=True)

    # user = db.relationship(carts, cascade="all, delete-orphan", backref=users)
    # users = db.relationship(
    #     "orderdetails", cascade="all, delete-orphan", backref="users"
    # )
    # users = db.relationship(orders, cascade="all, delete-orphan", backref=users)

    def __repr__(self):
        return {f"id = {self.id} users = {self.name}"}