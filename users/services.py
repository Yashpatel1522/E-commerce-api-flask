import config as db
import re
from .models import users

# =======================================================registration Validations==============================================
registrations_post_arguments = db.app.reqparse.RequestParser()
registrations_post_arguments.add_argument(
    "role", type=str, help="Enter Role :", required=True
)
registrations_post_arguments.add_argument(
    "name", type=str, help="Enter Name :", required=True
)
registrations_post_arguments.add_argument(
    "email", type=str, help="Enter Email :", required=True
)
registrations_post_arguments.add_argument(
    "contact", type=str, help="Enter Contact :", required=True
)
registrations_post_arguments.add_argument(
    "password", type=str, help="Enter password :", required=True
)
registrations_post_arguments.add_argument(
    "confrimpassword", type=str, help="Enter confrim password :", required=True
)


def is_num(data):
    return data.isnumeric()


EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
CONTACT = r"(0|91)?[6-9][0-9]{9}"


def check_email(email):
    if re.fullmatch(EMAIL, email):
        return False
    else:
        return True


def check_contact(number):
    if re.fullmatch(CONTACT, number):
        return False
    else:
        return True


class registrations(db.app.Resource):
    # ===================================================Add New User (Registration)==============================================

    def post(self):

        args = registrations_post_arguments.parse_args()
        if is_num(args["role"]):
            db.app.abort(400, message="Invalid Role")
        if is_num(args["name"]):
            db.app.abort(400, message="Invalid Name")
        print(check_email(args["email"]))
        if check_email(args["email"]):
            db.app.abort(400, message="Invalid Email")
        if check_contact(args["contact"]):
            db.app.abort(400, message="Invalid Contact")

        data = users.query.filter_by(email=args["email"]).first()
        if data:
            db.app.abort(409, message="Email Already Exists")

        if not (
            (len(args.password) >= 8 and (len(args.confrimpassword) >= 8))
            and (args.password == args.confrimpassword)
        ):
            db.app.abort(400, message="Passwords is Invalid")
        # print(len(args.password))
        try:
            result = users(
                role=args["role"],
                name=args["name"],
                email=args["email"],
                contact=args["contact"],
                password=args.password,
            )
            db.db.session.add(result)
            db.db.session.commit()
            return ({"flag": True, "message": "Data is Inserted"}, 200)
        except Exception as err:
            return err


# =======================================================login======================================================

login_post_request = db.app.reqparse.RequestParser()
login_post_request.add_argument("email", type=str, help="Enter Email", required=True)
login_post_request.add_argument(
    "password", type=str, help="Enter password", required=False
)


class login(db.app.Resource):
    # ===================================================Login==============================================

    def post(self):
        args = login_post_request.parse_args()
        result = users.query.filter_by(email=args.email).first()
        if not result:
            db.app.abort(404, message="Not Found")

        if not (result.password == args.password):
            db.app.abort(400, message="Wrong Password")

        db.app.login_status = {"email": args.email, "role": result.role}
        return {"flag": True, "message": "Successfully login...."}, 200


registration_bp = db.app.Blueprint("registration", __name__)
api = db.app.Api(registration_bp)
api.add_resource(registrations, "/registration")

login_bp = db.app.Blueprint("login", __name__)
api = db.app.Api(login_bp)
api.add_resource(login, "/login")
