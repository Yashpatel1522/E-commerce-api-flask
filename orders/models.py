import config as config

db = config.db

class orderdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return {f"id = {self.id} price = {self.price}"}
    
class orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.Date, nullable=False)

    # users = db.relationship(
    #     "orderdetails", cascade="all, delete-orphan", backref="orders"
    # )

    def __repr__(self):
        return {f"id = {self.id} price = {self.date}"}
