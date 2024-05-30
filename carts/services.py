import config as db
from users.models import users
from products.models import products
from carts.models import carts

add_to_cart = db.app.reqparse.RequestParser()
add_to_cart.add_argument(
    "product_id", type=int, help="please enter product di", required=True
)
add_to_cart.add_argument(
    "quantity", type=int, help="please enter quantity", required=True
)

get_cart_fields = {
    "product_name": db.app.fields.String,
    "id": db.app.fields.Integer,
    "product_id": db.app.fields.Integer,
    "user_id": db.app.fields.Integer,
    "quantity": db.app.fields.Integer,
}

update_data = db.app.reqparse.RequestParser()
update_data.add_argument("quantity", type=int, help="Invalid data..", required=True)


class cart(db.app.Resource):
    def post(self):
        if db.app.login_status:
            if (
                db.app.login_status["role"] == "admin"
                or db.app.login_status["role"] == "users"
            ):
                args = add_to_cart.parse_args()
                user_data = users.query.filter_by(
                    email=db.app.login_status["email"]
                ).first()
                product_data = products.query.filter_by(id=args.product_id).first()
                if product_data and product_data.quantity >= args.quantity:
                    result = carts(
                        product_id=product_data.id,
                        user_id=user_data.id,
                        quantity=args.quantity,
                    )
                    db.db.session.add(result)
                    db.db.session.commit()
                    return {"flag": True, "message": "added products into cart..."}, 200
                else:
                    db.app.abort(400, message="Invalid data......")
            else:
                db.app.abort(400, message="unauthorised user......")
        else:
            db.app.abort(400, message="login required......")

    @db.app.marshal_with(get_cart_fields)
    def get(self):
        if db.app.login_status:
            if (
                db.app.login_status["role"] == "admin"
                or db.app.login_status["role"] == "users"
            ):
                user_data = users.query.filter_by(
                    email=db.app.login_status["email"]
                ).first()
                cart_data = (
                    carts.query.join(products)
                    .filter(
                        carts.product_id == products.id, carts.user_id == user_data.id
                    )
                    .with_entities(
                        products.product_name,
                        carts.id,
                        carts.product_id,
                        carts.user_id,
                        carts.quantity,
                    )
                    .all()
                )
                if cart_data:
                    return cart_data
                else:
                    return {"flag": False, "message": "no data found"}, 404
            else:
                db.app.abort(400, message="unauthorised user......")
        else:
            db.app.abort(400, message="login required......")

    def delete(self, id):
        if db.app.login_status:
            if (
                db.app.login_status["role"] == "admin"
                or db.app.login_status["role"] == "users"
            ):
                user_data = users.query.filter_by(
                    email=db.app.login_status["email"]
                ).first()

                result = carts.query.filter_by(
                    user_id=user_data.id, product_id=id
                ).first()

                if result:
                    db.db.session.delete(result)
                    db.db.session.commit()
                    return {
                        "flag": True,
                        "message": "item deleted from carts.....",
                    }, 200
                else:
                    return {"flag": False, "message": "No data Found...."}, 400
            else:
                db.app.abort(400, message="unauthorised user......")
        else:
            db.app.abort(400, message="login required......")

    def patch(self, id):
        if db.app.login_status:
            if (
                db.app.login_status["role"] == "admin"
                or db.app.login_status["role"] == "users"
            ):
                args = update_data.parse_args()
                user_data = users.query.filter_by(
                    email=db.app.login_status["email"]
                ).first()
                result = carts.query.filter_by(
                    user_id=user_data.id, product_id=id
                ).first()
                product_data = products.query.filter_by(id=id).first()
                if result and product_data.quantity >= args.quantity:
                    result.quantity = args.quantity
                    db.db.session.add(result)
                    db.db.session.commit()
                    return {"flag": True, "message": "cart data is updated..."}, 200
                else:
                    return {"flag": False, "message": "invalid data"}, 400
            else:
                db.app.abort(400, message="unauthorised user......")
        else:
            db.app.abort(400, message="login required......")


cart_bp = db.app.Blueprint("cart", __name__)
api = db.app.Api(cart_bp)
api.add_resource(cart, "/cart", "/cart", "/cart/<int:id>", "/cart/<int:id>")
