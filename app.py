from flask import Flask,Blueprint
from flask_restful import Api,Resource,reqparse,marshal_with,fields,abort
login_status={}

app=Flask(__name__)
api=Api(app)

# import users.services as services   
from users.services import registration_bp,login_bp
from products.services import add_products_bp
from carts.services import cart_bp
from orders.services import order_bp

app.register_blueprint(registration_bp,url_prefix="/ecomm")
app.register_blueprint(login_bp,url_prefix="/ecomm")

app.register_blueprint(add_products_bp,url_prefix="/ecomm")

app.register_blueprint(cart_bp,url_prefix="/ecomm")

app.register_blueprint(order_bp,url_prefix="/ecomm")