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
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    profile = Column(String)  # Change To path For the Future

    categories = relationship("Category", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    incomes = relationship("Income", back_populates="user")
    budgets = relationship("Budget", back_populates="user")

    def to_json(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "profile": self.profile,
        }


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    total_amount = Column(Float)
    user_username = Column(String, ForeignKey('users.username'))

    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "total_amount": self.total_amount,
            "username": self.user_username
        }


class Expense(db.Model):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float, nullable=False)
    description = Column(String)
    date = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_username = Column(String, ForeignKey('users.username'))

    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "description": self.description,
            "date": self.date,
            "categoryId": self.category_id,
            "username": self.user_username
        }


class Income(db.Model):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float, nullable=False)
    date = Column(String)
    description = Column(String)
    user_username = Column(String, ForeignKey('users.username'))

    user = relationship("User", back_populates="incomes")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "date": self.date,
            "description": self.description,
            "username": self.user_username
        }


class Budget(db.Model):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer, nullable=False)
    description = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    username = Column(String, ForeignKey("users.username"))

    user = relationship("User", back_populates="budgets")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "username": self.username,
        }


@app.cli.command("db_create")
def create_db():
    db.create_all()
    print("database is created")


@app.cli.command("db_drop")
def drop_db():
    db.drop_all()
    print("database is dropped")


@app.cli.command("db_seed")
def seed_db():
    # Add users
    user1 = User(username='adnantabda',
                 first_name="adnan",
                 last_name="abda",
                 email="adnantabda@gmail.com",
                 password='adnan123',
                 profile="profile/20231027_115046.jpg")

    db.session.add(user1)

    # Add categories
    category1 = Category(name='Food', user=user1)
    category2 = Category(name='Shopping', user=user1)

    db.session.add(category1)
#
#     # Add expenses
    expense1 = Expense(amount=50.75,
                       description='Grocery shopping',
                       date=str(datetime.date.today()),
                       category=category1,
                       user=user1)
    expense2 = Expense(amount=15.00,
                       description='Shoes Nike',
                       date=str(datetime.date.today() - datetime.timedelta(days=1)),
                       category=category2,
                       user=user1)
    expense3 = Expense(amount=13.00,
                       description='T-shirt',
                       date=str(datetime.date.today() - datetime.timedelta(days=1)),
                       category=category2,
                       user=user1)
    expense4 = Expense(amount=50.00,
                       name="Adidas Full ",
                       description='premiumX Adidas',
                       date=str(datetime.date.today() - datetime.timedelta(days=1)),
                       category=category2,
                       user=user1)

    #Add Budget
    budget1 = Budget(name="school",
                     amount=250,
                     description="school fee",
                     start_date=(datetime.date.today() - datetime.timedelta(days=30)),
                     end_date=(datetime.date.today()),
                     user=user1
                     )
    budget2 = Budget(name="rent",
                     amount=500,
                     description="monthly room rent fee",
                     start_date=(datetime.date.today() - datetime.timedelta(days=30)),
                     end_date=(datetime.date.today()),
                     user=user1
                     )

    db.session.add_all([budget1, budget2])

    db.session.add_all([expense1, expense2, expense3, expense4])

    #Add income

    income1 = Income(name="Freelancing",
                     description="upwork freelancing jobs",
                     amount=12000,
                     date=datetime.date.today(),
                     user=user1)

    db.session.add(income1)

    db.session.commit()


@app.route("/")
def home():
    return jsonify(message="expenomy main server")


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


@app.route("/register", methods=["POST"])
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
        return jsonify(success=1), 201


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
            return jsonify(success=1, access_token=access_token), 201
    else:
        return jsonify(message="This username doesn't exist !!"), 401


# @app.route("/<username>")
# def user_page(username):
#     user = User.query.filter_by(username=username).first()
#     if user:
#         user = user.to_json()
#         return jsonify(user)
#     else:
#         return no_such_url(f"no such username as {username}")


@app.route("/<username>/dashboard")
@jwt_required()
def user_expenses(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized"), 403

    user = User.query.filter_by(username=username).first()
    if user:
        user_expenses_ = Expense.query.filter_by(user_username=username).all()
        user_expense = list(map(lambda x: x.to_json(), user_expenses_))
        user_categories = Category.query.filter_by(user_username=username).all()
        user_category = list(map(lambda x: x.to_json(), user_categories))
        user_budgets = Budget.query.filter_by(username=username).all()
        user_budget = list(map(lambda x: x.to_json(), user_budgets))
        user_incomes = Income.query.filter_by(user_username=username).all()
        user_income = list(map(lambda x: x.to_json(), user_incomes))
        return jsonify(expenses=user_expense, categories=user_category, budgets=user_budget, incomes=user_income)
    else:
        return jsonify(message="this username doesn't exits"), 404


@app.route("/<username>/categories")
@jwt_required()
def get_categories(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized"), 403

    user = User.query.filter_by(username=username).first()
    if user:
        user_categories = Category.query.filter_by(user_username=username).all()
        user_category = list(map(lambda x: x.to_json(), user_categories))
        return jsonify(categories=user_category)


@app.route("/<username>/categories/<category_id>", methods=['POST'])
@jwt_required()
def update_category(username: str, category_id: int):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message='not authorized ')

    category = Category.query.filter_by(id=category_id, user_username=username).first()
    if category:
        if request.form['name']:
            category.name = request.form['name']
        if request.form['description']:
            category.description = request.form['description']
        if request.form['total_amount']:
            category.total_amount = request.form['total_amount']

        db.session.commit()
        return jsonify(success=1), 202
    else:
        return jsonify(message="category doesn't exit"), 404


@app.route("/<username>/expenses")
@jwt_required()
def get_expenses(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    expenses = Expense.query.filter_by(user_username=username).all()
    expense = list(map(lambda x: x.to_json(), expenses))
    return jsonify(expense)


@app.route("/<username>/expenses/update/<id_>", methods=['PUT'])
@jwt_required()
def update_expenses(username, id_: int):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message='not authorized')
    expenses = Expense.query.filter_by(user_username=username, id=id_).first()
    if expenses:
        if request.form['name']:
            expenses.name = request.form['name']
        if request.form['amount']:
            expenses.amount = request.form['amount']
        if request.form['date']:
            expenses.date = request.form['date']
        if request.form['description']:
            expenses.description = request.form['description']
        db.session.commit()
        return jsonify(success=1)
    else:
        return jsonify(message="not found")


@app.route("/<string:username>/expenses/delete/<int:id_>", methods=["DELETE"])
@jwt_required()
def delete_expense(username, id_: int):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized")

    expense = Expense.query.filter_by(user_username=username, id=id_).first()
    if expense:
        if username == expense.user_username and expense.id == id_:
            db.session.delete(expense)
            db.session.commit()
            return jsonify(success=1)
        else:
            return jsonify(message="not successful")
    else:
        return jsonify(message="not found")


@app.errorhandler(404)
def no_such_url(e):
    return jsonify(error=e), 404


if __name__ == "__main__":
    app.run(debug=True)
