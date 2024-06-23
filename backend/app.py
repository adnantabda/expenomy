from flask import Flask, jsonify, request
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.orm import relationship
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "ExpenseTrackerDB.db")
app.config["JWT_SECRET_KEY"] = 'super_secret'
db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    __tablename__ = "users"

    username = Column(String, primary_key=True, nullable=False, unique=True)
    password = Column(String, nullable=False)

    categories = relationship("Category", back_populates="user")
    expenses = relationship("Expense", back_populates="user")

    def to_json(self):
        return {
            "username": self.username,
            "password": self.password
        }


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_username = Column(Integer, ForeignKey('users.username'))

    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.user_username
        }


class Expense(db.Model):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    description = Column(String)
    date = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_username = Column(Integer, ForeignKey('users.username'))

    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")

    def to_json(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "date": self.date,
            "categoryId": self.category_id,
            "username": self.user_username
        }


# @app.cli.command("db_create")
# def create_db():
#     db.create_all()
#     print("database is created")
#
#
# @app.cli.command("db_drop")
# def drop_db():
#     db.drop_all()
#     print("database is dropped")
#
#
# @app.cli.command("db_seed")
# def seed_db():
#     # Add users
#     user1 = User(username='john_doe', password='password123')
#     user2 = User(username='jane_smith', password='password123')
#     user3 = User(username='alice_jones', password='password123')
#     user4 = User(username='bob_brown', password='password123')
#
#     db.session.add_all([user1, user2, user3, user4])
#
#     # Add categories
#     category1 = Category(name='Food', user=user1)
#     category2 = Category(name='Transport', user=user1)
#     category3 = Category(name='Utilities', user=user1)
#     category4 = Category(name='Entertainment', user=user2)
#     category5 = Category(name='Healthcare', user=user3)
#     category6 = Category(name='Education', user=user3)
#     category7 = Category(name='Clothing', user=user4)
#     category8 = Category(name='Travel', user=user4)
#     category9 = Category(name='Miscellaneous', user=user4)
#     category10 = Category(name='Savings', user=user4)
#
#     db.session.add_all([category1, category2, category3, category4,
#                         category5, category6, category7, category8, category9, category10])
#
#     # Add expenses
#     expense1 = Expense(amount=50.75, description='Grocery shopping', date=str(datetime.date.today()),
#                        category=category1, user=user1)
#     expense2 = Expense(amount=15.00, description='Bus fare',
#                        date=str(datetime.date.today() - datetime.timedelta(days=1)), category=category2, user=user2)
#     expense3 = Expense(amount=120.00, description='Electricity bill',
#                        date=str(datetime.date.today() - datetime.timedelta(days=2)), category=category3, user=user3)
#     expense4 = Expense(amount=60.00, description='Movie tickets',
#                        date=str(datetime.date.today() - datetime.timedelta(days=3)), category=category4, user=user4)
#     expense5 = Expense(amount=30.00, description='Doctor visit',
#                        date=str(datetime.date.today() - datetime.timedelta(days=4)), category=category5, user=user1)
#     expense6 = Expense(amount=200.00, description='Course fee',
#                        date=str(datetime.date.today() - datetime.timedelta(days=5)), category=category6, user=user1)
#     expense7 = Expense(amount=45.00, description='New shoes',
#                        date=str(datetime.date.today() - datetime.timedelta(days=6)), category=category7, user=user2)
#     expense8 = Expense(amount=500.00, description='Flight ticket',
#                        date=str(datetime.date.today() - datetime.timedelta(days=7)), category=category8, user=user3)
#     expense9 = Expense(amount=25.00, description='Birthday gift',
#                        date=str(datetime.date.today() - datetime.timedelta(days=8)), category=category9, user=user4)
#     expense10 = Expense(amount=150.00, description='Savings deposit',
#                         date=str(datetime.date.today() - datetime.timedelta(days=9)), category=category10, user=user1)
#
#     db.session.add_all([expense1, expense2, expense3, expense4, expense5,
#                         expense6, expense7, expense8, expense9, expense10])
#
#     db.session.commit()


@app.route("/")
def home():
    return jsonify(message="The name is Foo")


# @app.route("/expenses", methods=['GET'])
# def get_expenses():
#     expenses = Expense.query.all()
#     json_expenses = list(map(lambda x: x.to_json(), expenses))
#     return jsonify({"expenses": json_expenses})


# @app.route("/users", methods=['GET'])
# def get_users():
#     users = User.query.all()
#     json_users = list(map(lambda x: x.to_json(), users))
#     return jsonify({"users": json_users})


@app.route( "/register", methods=["POST"])
def register():
    username = request.form['username']
    test = User.query.filter_by(username=username).first()
    if test:
        return jsonify(message="This user already exists !!"), 409
    else:
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully ") , 201


@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    test = User.query.filter_by(username=username).first()
    if test:
        password = request.form['password']
        data_password = test.to_json()['password']
        if data_password != password:
            return jsonify(message="Incorrect password !!")
        else:
            access_token = create_access_token(identity=username)
            return jsonify(message="Login succeeded ", access_token=access_token)
    else:
        return jsonify(message="This username doesn't exist !!"), 401


@app.route("/<username>")
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user = user.to_json()
        return jsonify(user)
    else:
        return no_such_url(f"no such username as {username}")


@app.route("/<username>/expenses")
@jwt_required()
def user_expenses(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="Not Authorized "), 403

    user = User.query.filter_by(username=username).first()
    if user:
        use_expenses = Expense.query.filter_by(user_username=username).all()
        use_expense = list(map(lambda x: x.to_json(), use_expenses))
        return jsonify(expenses=use_expense)
    else:
        return jsonify(message="this username doesn't exits"), 404


@app.route("/<username>/categories")
@jwt_required()
def get_categories(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify("Not Authorized !!"), 403

    user = User.query.filter_by(username=username).first()
    if user:
        user_categories = Category.query.filter_by(user_username=username).all()
        user_category = list(map(lambda x: x.to_json(), user_categories))
        return jsonify(categories=user_category)


@app.errorhandler(404)
def no_such_url(e):
    return jsonify(error=e), 404


if __name__ == "__main__":
    app.run(debug=True)
