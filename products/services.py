import config as db
from users.services import is_num

add_products_resources=db.app.reqparse.RequestParser()
add_products_resources.add_argument("product_name",type=str,help="Please enter product name",required=True)
add_products_resources.add_argument("quantity",type=int,help="Please enter products quantity",required=True)
add_products_resources.add_argument("price",type=int,help="please enter products price",required=True)

class add_products(db.app.Resource):
    def post(self):
        args=add_products_resources.parse_args()
        if is_num(args.product_name):
            db.app.abort(400,message="please enter valid input for products n   ame")

add_products_bp=db.app.Blueprint("add_products",__name__)


