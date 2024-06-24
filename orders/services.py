import config as db
from carts.models import carts
from users.models import users
from products.models import products
from .models import orders, orderdetails
from datetime import datetime

get_cart_fields = {
    "product_name": db.app.fields.String,
    "id": db.app.fields.Integer,
    "product_id": db.app.fields.Integer,
    "user_id": db.app.fields.Integer,
    "quantity": db.app.fields.Integer,
}


class order(db.app.Resource):
    @db.app.marshal_with(get_cart_fields)
    def post(self):
        if db.app.login_status:
            if db.app.login_status["role"] == "users":
                user_data = users.query.filter_by(
                    email=db.app.login_status["email"]
                ).first()
                cart_data = (
                    carts.query.join(products)
                    .filter(
                        carts.product_id == products.id, carts.user_id == user_data.id
                    )
                    .with_entities(
                        carts.product_id,
                        carts.quantity,
                        products.product_name,
                        products.price,
                    )
                    .all()
                )

                for i in cart_data:
                    result = products.query.filter_by(id=i[0]).first()
                    if result.quantity < i[1]:
                        db.app.abort(
                            400,
                            message=f"invalid quantity... please go to cart and update {i[2]}  quantity",
                        )

                result = orders(user_id=user_data.id, date=datetime.now())
                db.db.session.add(result)
                db.db.session.commit()

                last_inserted_id = result.id

                for i in cart_data:
                    result = orderdetails(
                        order_id=last_inserted_id,
                        product_id=i[0],
                        date=datetime.now(),
                        price=i[3],
                    )
                    result2 = carts.query.filter(
                        carts.product_id == i[0], carts.user_id == user_data.id
                    ).first()
                    db.db.session.add(result)
                    db.db.session.delete(result2)
                    db.db.session.commit()

                db.app.abort(200, message="order placed....")
            else:
                db.app.abort(400, message="unauthorised user......")
        else:
            db.app.abort(400, message="login required......")


order_bp = db.app.Blueprint("orders", __name__)

api = db.app.Api(order_bp)
api.add_resource(order, "/order")
