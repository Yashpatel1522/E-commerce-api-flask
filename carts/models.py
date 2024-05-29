import config as config


db = config.db


class carts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return {f"id = {self.id} products = {self.products}"}