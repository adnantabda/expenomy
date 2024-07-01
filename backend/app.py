from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import User, Expense, Category, Income, Budget
from config import db
from config import app
import datetime
from flask import request, jsonify


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
    return "<h1> expenomy main server </h1>"

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
    email = request.form['email']
    test = User.query.filter_by(username=username).first()
    test_email = User.query.filter_by(email=email).first()

    if test:
        return jsonify(message="This username already exists !!"), 409
    if test_email:
        return jsonify(message="email already exists !!")

    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    user = User(username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email)

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
@app.route("/<username>/delete", methods=["DELETE"])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(success=1)

    else:
        return jsonify(message="user doesn't exist")


@app.route("/<username>/dashboard")
@jwt_required()
def user_dashboard(username):
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


@app.route("/<username>/categories/create", methods=['POST'])
@jwt_required()
def create_categories(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    name = request.form['name']
    description = request.form['description']
    new_category = Category(name=name,
                            description=description,
                            user_username=username)

    db.session.add(new_category)
    db.session.commit()
    return jsonify(success=1)


@app.route("/<username>/categories/update/<category_id>", methods=['POST'])
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


@app.route("/<string:username>/categories/delete/<int:category_id>", methods=['DELETE'])
@jwt_required()
def delete_category(username: str, category_id: int):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized !!")

    category = Category.query.filter_by(id=category_id, user_username=username).first()
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify(success=1)
    else:
        return jsonify(message="not success")


@app.route("/<username>/expenses")
@jwt_required()
def get_expenses(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    expenses = Expense.query.filter_by(user_username=username).all()
    expense = list(map(lambda x: x.to_json(), expenses))
    return jsonify(expenses=expense)


@app.route("/<username>/expenses/update/<id_>", methods=['PUT'])
@jwt_required()
def update_expenses(username, id_: int):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message='not authorized'), 403

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
        return jsonify(message="not found"), 404


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


@app.route("/<username>/expenses/create", methods=['POST'])
@jwt_required()
def create_expense(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    name = request.form['name']
    amount = float(request.form['amount'])
    description = request.form['description']
    date = request.form['date']
    user_username = username
    new_expense = Expense(name=name,
                          amount=amount,
                          description=description,
                          date=date,
                          user_username=user_username)

    db.session.add(new_expense)
    db.session.commit()
    return jsonify(success=1)


@app.route("/<username>/budgets", methods=['GET'])
@jwt_required()
def get_budgets(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    budgets = Budget.query.filter_by(username=username).all()
    budget = list(map(lambda x: x.to_json(), budgets))
    return jsonify(budgets=budget)


@app.route("/<username>/budgets/create", methods=['POST'])
@jwt_required()
def create_budgets(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    name = request.form['name']
    description = request.form['description']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    amount = request.form['amount']

    new_budget = Budget(name=name,
                        username=username,
                        description=description,
                        start_date=start_date,
                        end_date=end_date,
                        amount=amount)

    db.session.add(new_budget)
    db.session.commit()
    return jsonify(success=1)


@app.route("/<username>/budgets/update/<int:budget_id>", methods=['PUT'])
@jwt_required()
def update_budget(username, budget_id: int):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    budget = Budget.query.filter_by(username=username, id=budget_id).first()
    if budget:
        if budget.id == budget_id and budget.username == username:
            budget.name = request.form['name']
            budget.description = request.form['description']
            budget.amount = request.form['amount']
            budget.start_date = request.form['start_date']
            budget.end_date = request.form['end_date']
            db.session.commit()
            return jsonify(success=1)
        else:
            return jsonify(message="can't access ")
    else:
        return jsonify(message="not found")


@app.route("/<username>/budgets/delete/<int:budget_id>", methods=['DELETE'])
@jwt_required()
def delete_budget(username, budget_id: int):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    budget = Budget.query.filter_by(username=username, id=budget_id).first()
    if budget:
        if budget.id == budget_id and budget.username == username:
            db.session.delete(budget)
            db.session.commit()
            return jsonify(success=1)
        else:
            return jsonify(message="not success")
    else:
        return jsonify(message="not found")


@app.route("/<username>/incomes", methods=['GET'])
@jwt_required()
def get_incomes(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    incomes = Income.query.filter_by(user_username=username).all()
    income = list(map(lambda x: x.to_json(), incomes))
    return jsonify(incomes=income)


@app.route("/<username>/incomes/create", methods=['POST'])
def create_incomes(username):
    name = request.form['name']
    amount = float(request.form['amount'])
    description = request.form['description']
    date = request.form['date']

    new_income = Income(name=name,
                        amount=amount,
                        date=date,
                        description=description,
                        user_username=username)

    db.session.add(new_income)
    db.session.commit()
    return jsonify(success=1)


@app.route("/<username>/incomes/update/<int:income_id>", methods=['PUT'])
@jwt_required()
def update_incomes(username, income_id: int):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    income = Income.query.filter_by(user_username=username, id=income_id).first()
    if income:
        income.name = request.form['name']
        income.description = request.form['description']
        income.amount = request.form['amount']
        income.date = request.form['date']

        db.session.commit()
        return jsonify(success=1)
    else:
        return jsonify(message="not found")


@app.route("/<username>/incomes/delete/<int:income_id>", methods=['DELETE'])
@jwt_required()
def delete_incomes(username, income_id: int):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify(message="not authorized ")

    income = Income.query.filter_by(user_username=username, id=income_id).first()
    if income:
        if income.user_username == username and income.id == income_id:
            db.session.delete(income)
            db.session.commit()
            return jsonify(success=1)
        else:
            return jsonify(message="not allowed")
    else:
        return jsonify(message="doesn't exist")


@app.errorhandler(404)
def not_found(error):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
