import config as db
from users.services import is_num
from app import login_status
from users.models import users
from .models import products

add_products_resources = db.app.reqparse.RequestParser()
add_products_resources.add_argument(
    "product_name", type=str, help="Please enter product name", required=True
)
add_products_resources.add_argument(
    "quantity", type=int, help="Please enter products quantity", required=True
)
add_products_resources.add_argument(
    "price", type=int, help="please enter products price", required=True
)

update_products_resources = db.app.reqparse.RequestParser()
update_products_resources.add_argument("product_name", type=str)
update_products_resources.add_argument("quantity", type=int)
update_products_resources.add_argument("price", type=int)

get_resources_fields = {
    "id": db.app.fields.Integer,
    "product_name": db.app.fields.String,
    "quantity": db.app.fields.Integer,
    "price": db.app.fields.Integer,
}


# ===================================================add product==============================================
class add_products(db.app.Resource):
    def post(self):
        if db.app.login_status:
            if db.app.login_status["role"] == "admin":

                args = add_products_resources.parse_args()
                print(args)
                if is_num(args.product_name):
                    db.app.abort(
                        400, message="please enter valid input for products name"
                    )
                result = products(
                    product_name=args.product_name,
                    quantity=args.quantity,
                    price=args.price,
                )
                db.db.session.add(result)
                db.db.session.commit()
                return {"flag": True, "message": "Products Added....."}, 200
            else:
                db.app.abort(400, message="unauthorised user......")
        else:
            db.app.abort(400, message="login required......")

    @db.app.marshal_with(get_resources_fields)
    def get(self):
        if db.app.login_status:
            if db.app.login_status["role"] == "admin":
                result = products.query.all()
                if result:
                    return result
                else:
                    return 204
            else:
                db.app.abort(400, message="unauthorised user......")
        else:
            db.app.abort(400, message="login required......")

    # @db.app.marshal_with(patch_resources_fields)
    def patch(self, id):
        if db.app.login_status:
            if db.app.login_status["role"] == "admin":
                result = products.query.filter_by(id=id).first()
                args = update_products_resources.parse_args()
                if not result:
                    db.app.abort(404, message="Not Found....")
                print(args)
                if (
                    args.product_name == None
                    and args.quantity == None
                    and args.price == None
                ):
                    db.app.abort(400, message="Content is Empty")
                if args.product_name:
                    result.product_name = args.product_name
                if args.quantity:
                    result.quantity = args.quantity
                if args.price:
                    result.price = args.price
                
                db.db.session.add(result)
                db.db.session.commit()
                return {
                    "flag":True,
                    "message":"data updated....."
                },200
            else:
                db.app.abort(400, message="unauthorised user......")
        else:
            db.app.abort(400, message="login required......")


# ===================================================get products==============================================


add_products_bp = db.app.Blueprint("add_products", __name__)
api = db.app.Api(add_products_bp)
api.add_resource(add_products, "/products", "/products", "/products/<int:id>")


# get_products_db=db.app.Blueprint("get_products",__name__)
# api=db.app.Api(get_products_db)
# api.add_resource(get_products,"/products")
