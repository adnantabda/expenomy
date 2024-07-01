from flask_jwt_extended import JWTManager
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "ExpenseTrackerDB.db")
app.config["JWT_SECRET_KEY"] = "6dd2c7f7fa08de2d898297a11b0e74db3c57b0b5672e3c9cb2a18aaaf1208eb3"
db = SQLAlchemy(app)
CORS(app)
jwt = JWTManager(app)
