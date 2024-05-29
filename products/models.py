import config as config



db = config.db


class products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=True)

    product = db.relationship("carts", cascade="all, delete-orphan", backref="products")
    products = db.relationship(
        "orderdetails", cascade="all, delete-orphan", backref="products"
    )

    def __repr__(self):
        return f"id = {self.id}  product name = {self.product_name}"
