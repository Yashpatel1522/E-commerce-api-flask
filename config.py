from flask_sqlalchemy import SQLAlchemy 
import app

app.app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:Dev%40123@localhost:5432/flask_ecom"
)
db = SQLAlchemy(app.app)

# with app.app.app_context():
#     db.create_all() 